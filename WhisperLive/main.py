from fastapi import FastAPI, HTTPException
from whisper_live.client import TranscriptionClient,Client
import socketio, librosa
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server = TranscriptionClient(
        "51.20.53.119",
        9090,
        lang="en",
        translate=True,
        model="small",
    )

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app.mount("/", socketio.ASGIApp(sio))

audio_bytes_gb = b""



def main_work_flow(audio_bytes):
    # print(len(audio_bytes['data']))
    # with open("audio.wav", "wb") as f:
    #     f.write(audio_bytes['data'])
    # print(audio_bytes)
    # print(audio_bytes['data'].size())
    # print(audio_bytes['data'].__len__()/4096)
    # audio_data = resample_audio(audio_bytes['data'])
    server.client.audio_stream(audio_bytes['data'],filename = "audio.wav")


@sio.on("transcribe")
def transcribe(sid,audio_bytes):
    main_work_flow(audio_bytes)

    
@sio.on("test")
def test(sid):
    print("Test")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
