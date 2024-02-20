from fastapi import FastAPI, HTTPException
from whisper_live.client import TranscriptionClient
from fastapi.responses import HTMLResponse
import socketio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = TranscriptionClient(
        "13.53.206.4",
        9090,
        lang="en",
        translate=False,
        model="small",
    )

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi")
# Mount Socket.IO server as a sub-application
app.mount("/socket.io", socketio.ASGIApp(sio))

# Define the event handler for the 'transcribe' event
@sio.on("transcribe")
def transcribe(sid,audio_bytes):
    # print(f"Received data: {data}")
    # response = client(audio_bytes)
    print("Transcribing")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
