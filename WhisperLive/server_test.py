from whisper_live.client import TranscriptionClient,Client

def test():
    server = TranscriptionClient(
            "51.20.53.119",
            9090,
            lang="en",
            translate=False,
            model="small",
        )
    print("[INFO]: Waiting for server ready ...")
    while not server.client.recording:
        if server.client.waiting or server.client.server_error:
            server.client.close_websocket()
            return
    server.client.play_file("audio_resampled.wav")
    print(server.client.transcript)

if __name__ == "__main__":
    test()

