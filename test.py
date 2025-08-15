from recordboy import RecordBoy

# Global test config
config = {
    "video_file": "test_video.avi",
    "events_file": "test_events.txt",
    "fps": 30,
    "screen": {"top": 0, "left": 0, "width": 1920, "height": 1080},
}


def run_test_init():
    print("Testing init...")
    print(f"Test config: {config}")

    try:
        RecordBoy(config=config)
    except ValueError as e:
        print(f"Init test failed: {e}")
    else:
        print("Init test passed.")


if __name__ == "__main__":
    print("Running tests...")
    run_test_init()
