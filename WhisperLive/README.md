# Audio Transcription with FastAPI and Socket.IO

This project demonstrates how to transcribe audio data captured from the browser using the Web Audio API, and sending it to a FastAPI backend server for transcription using Socket.IO.

## Prerequisites

- Python 3.x installed on your machine.

## Setup

### Backend (FastAPI)

1. Install the required Python packages using pip:

    ```
    cd requirements
    pip install -r client.txt
    ```

2. Run the FastAPI backend server:

    ```
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```


## Usage

1. Open the webpage on live server.

2. Click on the "Start Capture" button to start recording audio.

3. Speak into your microphone to capture audio. The audio will be automatically sent to the backend for transcription.

4. Click on the "Stop Capture" button to stop recording audio.

5. The transcription result will be displayed in the browser window.

## Architecture

- The backend server is built using FastAPI, a modern web framework for building APIs with Python.
- Socket.IO is used for real-time communication between the frontend and backend.
- The frontend consists of an HTML page with JavaScript code that captures audio using the Web Audio API and sends it to the backend server for transcription.


