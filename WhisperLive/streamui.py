import logging
import queue
from whisper_live.client import TranscriptionClient, Client
import matplotlib.pyplot as plt
import numpy as np
import pydub
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import librosa
import time

logger = logging.getLogger(__name__)
server = None
last_message_time = time.time()  # Initialize the last message time

@st.cache_resource
def start_server():
    global server
    server = TranscriptionClient(
        "51.20.53.119",
        9090,
        lang="en",
        translate=True,
        model="small",
    )
    return server

def read_text_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()

def clear_text_file(file_path: str):
    with open(file_path, "w") as file:
        file.write("")


def audio_frame_to_np_buffer(frames, target_sample_rate=None, mono=False):
    arrays = []

    for frame in frames:
        num_channels = len(frame.layout.channels)
        np_frame = np.frombuffer(frame.planes[0].to_bytes(), dtype=np.int16).reshape(
            -1, num_channels
        )
        if mono:
            np_frame = np.mean(np_frame, axis=1).astype(np.int16)
        if target_sample_rate is not None and target_sample_rate != frame.sample_rate:
            np_frame = np_frame.astype(np.float32) / 32768
            np_frame = librosa.resample(
                np_frame.T, orig_sr=frame.sample_rate, target_sr=target_sample_rate
            )
            if mono:
                np_frame = np_frame[np.newaxis, :]
            np_frame = (np_frame * 32768).astype(np.int16)

        arrays.append(np_frame)

    combined_buffer = np.concatenate(arrays, axis=0)

    return combined_buffer


st.title("WhisperLive")

start_server()
time.sleep(5)
webrtc_ctx = webrtc_streamer(
    key="sendonly-audio",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    media_stream_constraints={"audio": True},
)

# text_box = st.empty()
text = ""
last_message_text = None  # Initialize the last message text
sound_window_len = 5000
sound_window_buffer = None



while True:
    clear_text_file("output_transcription.txt")
    if webrtc_ctx.audio_receiver:
        try:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        except queue.Empty:
            logger.warning("Queue is empty. Abort.")
            break

        sound_chunk = pydub.AudioSegment.empty()
        if len(audio_frames) == 0:
            continue

        np_buffer = audio_frame_to_np_buffer(
            audio_frames, target_sample_rate=16000, mono=True
        )
        start_server().client.audio_stream(np_buffer, filename="audio.wav")
        for audio_frame in audio_frames:
            sound = pydub.AudioSegment(
                data=audio_frame.to_ndarray().tobytes(),
                sample_width=audio_frame.format.bytes,
                frame_rate=audio_frame.sample_rate,
                channels=len(audio_frame.layout.channels),
            )
            sound_chunk += sound

        if len(sound_chunk) > 0:
            if sound_window_buffer is None:
                sound_window_buffer = pydub.AudioSegment.silent(
                    duration=sound_window_len
                )

            sound_window_buffer += sound_chunk
            if len(sound_window_buffer) > sound_window_len:
                sound_window_buffer = sound_window_buffer[-sound_window_len:]

        # Check if 4 seconds have elapsed since the last message

        new_words = read_text_file("output_transcription.txt")
        if last_message_text == new_words:

                continue
        else:
            if time.time() - last_message_time > 5:

                
                clear_text_file("output_transcription.txt")
                if new_words:
                    # Display a new message
                    last_message_text = new_words
                    with st.chat_message("user"):
                        st.write(last_message_text)
                    last_message_time = time.time()
            else:
                # Update the existing message
                clear_text_file("output_transcription.txt")
                if new_words:
                    last_message_text = new_words
                    with st.chat_message("user"):
                        st.write(last_message_text)

    else:
        with open("output_transcription.txt", "w") as file:
            file.write("")
        break
