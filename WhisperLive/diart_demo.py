from diart import SpeakerDiarization
from diart.sources import MicrophoneAudioSource, FileAudioSource
from diart.inference import StreamingInference

pipeline = SpeakerDiarization()
mic = MicrophoneAudioSource()
wavfile = FileAudioSource("output.wav", sample_rate=16000)
# inference = StreamingInference(pipeline, mic, do_plot=True)
inference = StreamingInference(pipeline, wavfile, do_plot=True)
prediction = inference()
with open("output_transcription.txt", "w") as f:
    f.write(str(prediction))