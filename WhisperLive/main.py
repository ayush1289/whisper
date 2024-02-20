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

def get_transcription(host:str,audio_bytes):
    client = TranscriptionClient(
        host,
        9090,
        lang="en",
        translate=False,
        model="small",
        audio_bytes= audio_bytes,
    )
    response = client()

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi")
# Mount Socket.IO server as a sub-application
app.mount("/socket.io", socketio.ASGIApp(sio))

# Define the event handler for the 'transcribe' event
@sio.on("transcribe")
def transcribe(sid, data):
    print(f"Received data: {data}")
    get_transcription("13.53.206.4",data)
    # Emit the 'transcribe' event to all connected clients

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
