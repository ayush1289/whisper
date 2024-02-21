from whisper_live.client import TranscriptionClient,Client

def test():
    server = TranscriptionClient(
            "13.60.22.43",
            9090,
            lang="en",
            translate=False,
            model="small",
        )
    server()


if __name__ == "__main__":
    test()

