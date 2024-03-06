"""A sample to use WebRTC in sendonly mode to transfer audio frames
from the browser to the server and visualize them with matplotlib
and `st.pyplot`."""

import logging
import queue
from whisper_live.client import TranscriptionClient,Client
import matplotlib.pyplot as plt
import numpy as np
import pydub
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import av
import librosa
# from sample_utils.turn import get_ice_servers

logger = logging.getLogger(__name__)
server = None

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
start_server()
webrtc_ctx = webrtc_streamer(
    key="sendonly-audio",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    # rtc_configuration={"iceServers": get_ice_servers()},
    media_stream_constraints={"audio": True},
)

def audio_frame_to_np_buffer(frames, target_sample_rate=None, mono=False):
    arrays = []
    
    for frame in frames:
        # Determine the number of channels from the frame layout
        num_channels = len(frame.layout.channels)
        
        # Convert each frame to a NumPy array, properly accounting for the number of channels
        np_frame = np.frombuffer(frame.planes[0].to_bytes(), dtype=np.int16).reshape(-1, num_channels)
        
        # If converting to mono, average the channels
        if mono:
            np_frame = np.mean(np_frame, axis=1).astype(np.int16)  # Ensure dtype stays as int16 after averaging
        
        # If resampling is required, perform the resampling on each frame's buffer
        if target_sample_rate is not None and target_sample_rate != frame.sample_rate:
            # Convert to float32 and normalize before resampling
            np_frame = np_frame.astype(np.float32) / 32768  
            # Resample
            np_frame = librosa.resample(np_frame.T, orig_sr=frame.sample_rate, target_sr=target_sample_rate)
            if mono:
                # Ensure mono output is a single row when mono=True
                np_frame = np_frame[np.newaxis, :]
            # De-normalize and convert back to int16
            np_frame = (np_frame * 32768).astype(np.int16)
        
        arrays.append(np_frame)
    
    # Concatenate all frame arrays into a single buffer
    combined_buffer = np.concatenate(arrays, axis=0)
    
    return combined_buffer

fig_place = st.empty()

fig, [ax_time, ax_freq] = plt.subplots(2, 1, gridspec_kw={"top": 1.5, "bottom": 0.2})

sound_window_len = 5000  # 5s
sound_window_buffer = None
while True:
    if webrtc_ctx.audio_receiver:
        try:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        except queue.Empty:
            logger.warning("Queue is empty. Abort.")
            break

        sound_chunk = pydub.AudioSegment.empty()
        if len(audio_frames) ==0:
            continue
        sr = start_server()

        np_buffer = audio_frame_to_np_buffer(audio_frames, target_sample_rate=16000, mono=True)
        sr.client.audio_stream(np_buffer,filename = "audio.wav")
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

        if sound_window_buffer:
            # Ref: https://own-search-and-study.xyz/2017/10/27/python%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E9%9F%B3%E5%A3%B0%E3%83%87%E3%83%BC%E3%82%BF%E3%81%8B%E3%82%89%E3%82%B9%E3%83%9A%E3%82%AF%E3%83%88%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%82%92%E4%BD%9C/  # noqa
            sound_window_buffer = sound_window_buffer.set_channels(1)  # Stereo to mono
            sample = np.array(sound_window_buffer.get_array_of_samples())

            ax_time.cla()
            times = (np.arange(-len(sample), 0)) / sound_window_buffer.frame_rate
            ax_time.plot(times, sample)
            ax_time.set_xlabel("Time")
            ax_time.set_ylabel("Magnitude")

            spec = np.fft.fft(sample)
            freq = np.fft.fftfreq(sample.shape[0], 1.0 / sound_chunk.frame_rate)
            freq = freq[: int(freq.shape[0] / 2)]
            spec = spec[: int(spec.shape[0] / 2)]
            spec[0] = spec[0] / 2

            ax_freq.cla()
            ax_freq.plot(freq, np.abs(spec))
            ax_freq.set_xlabel("Frequency")
            ax_freq.set_yscale("log")
            ax_freq.set_ylabel("Magnitude")

            fig_place.pyplot(fig)
    else:
        # logger.warning("AudioReciver is not set. Abort.")
        break