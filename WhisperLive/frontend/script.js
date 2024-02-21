import { serve } from "https://deno.land/std@0.166.0/http/server.ts";
import { Server } from "https://deno.land/x/socket_io@0.2.0/mod.ts";

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Get the startCapture button
    const startCaptureButton = document.getElementById('startCapture');
    // Get the stopCapture button
    const stopCaptureButton = document.getElementById('stopCapture');
    // Initialize variable to hold recorded audio data
    let recordedChunks = [];
    // Get the audio stream from the user's microphone
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function (stream) {
            // Create a new MediaRecorder instance, which will be used to record the audio
            const mediaRecorder = new MediaRecorder(stream);
            // Create a new Socket.IO connection
            const io = new Server(); // Connect to the Socket.io server
            // When the startCapture button is clicked
            startCaptureButton.addEventListener('click', function () {
                // Start recording the audio
                mediaRecorder.start();
                // Log the start of the recording
                console.log('Recording started');
            });
            // When the stopCapture button is clicked
            stopCaptureButton.addEventListener('click', function () {
                // Stop recording the audio
                mediaRecorder.stop();
                // Log the end of the recording
                console.log('Recording stopped');
            });
            // When the MediaRecorder has data available
            mediaRecorder.ondataavailable = function (event) {
                // Push the recorded chunk into the recordedChunks array
                recordedChunks.push(event.data);
            };
            // When the MediaRecorder stops recording
            mediaRecorder.onstop = function () {
                // Create a new Blob from the recorded chunks
                const audioBlob = new Blob(recordedChunks);
                // Read the Blob as a data URL
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                // When the data URL is ready
                reader.onloadend = function () {
                    // Get the base64 encoded audio data
                    const base64data = reader.result.split(',')[1];
                    // Send the audio data to the server
                    socket.emit('audio', { audioData: base64data });
                };
                // Clear the recordedChunks array for the next recording
                recordedChunks = [];
            };
        })
        .catch(function (error) {
            // Log any errors
            console.error('Error accessing the microphone', error);
        });
});
