from fastapi import FastAPI, HTTPException
from whisper_live.client import TranscriptionClient,Client
from fastapi.responses import HTMLResponse
import socketio
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

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
        "13.60.22.43",
        9090,
        lang="en",
        translate=False,
        model="small",
    )

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
# Mount Socket.IO server as a sub-application
app.mount("/", socketio.ASGIApp(sio))

# Define the event handler for the 'transcribe' event
@sio.on("transcribe")
def transcribe(sid,audio_bytes):
    audio_bytes =(audio_bytes['data'])
    # with open("audio.wav", "bx") as f:
    #     f.write(audio_bytes)
    server.client.audio_stream(audio_bytes)

    
    
sio.on("test")
def test(sid):
    print("Test")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
