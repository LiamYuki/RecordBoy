from recordboy import RecordBoy
from pynput import mouse, keyboard

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


def run_test_getters_setters():
    print("Testing getters and setters...")
    recordboy = RecordBoy(config=config)

    # Test getting config
    assert recordboy.get_config() == config
    print("Get config test passed.")

    # Test getting path
    assert recordboy.get_path() == None
    print("Get path test passed.")

    # Test setting config
    new_config = {
        "video_file": "new_video.avi",
        "events_file": "new_events.txt",
        "fps": 60,
        "screen": {"top": 0, "left": 0, "width": 1280, "height": 720},
    }
    recordboy.set_config(new_config)
    assert recordboy.get_config() == new_config
    print("Set config test passed.")

    # Test setting path
    recordboy.set_path("new_path.avi")
    assert recordboy.get_path() == "new_path.avi"
    print("Set path test passed.")


def run_test_listeners():
    print("Testing listeners...")
    recordboy = RecordBoy(config=config)

    # Start recording
    recordboy.record()

    # Simulate mouse and keyboard events
    # These would normally be triggered by actual user input
    recordboy._on_move(100, 200)
    recordboy._on_click(100, 200, mouse.Button.left, True)
    recordboy._on_scroll(100, 200, 0, -1)
    recordboy._on_press(keyboard.Key.enter)
    recordboy._on_release(keyboard.Key.enter)

    # Check recorded events
    assert len(recordboy.events) > 0
    print("Listeners test passed.")


if __name__ == "__main__":
    print("Running tests...")
    run_test_init()
    run_test_getters_setters()
    run_test_listeners()
