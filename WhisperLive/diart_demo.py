from diart import SpeakerDiarization
from diart.sources import MicrophoneAudioSource, FileAudioSource, AudioStreamSource
from diart.inference import StreamingInference

pipeline = SpeakerDiarization()

mic = MicrophoneAudioSource()
wavfile = FileAudioSource("output.wav", sample_rate=16000)
# stream = AudioStreamSource(audio_bytes, sample_rate=16000)

# inference = StreamingInference(pipeline, mic, do_plot=True)
# inference = StreamingInference(pipeline, wavfile, do_plot=True)
inference = StreamingInference(pipeline, mic, do_plot=False)
prediction = inference()
with open("output_transcription.txt", "w") as f:
    f.write(str(prediction))