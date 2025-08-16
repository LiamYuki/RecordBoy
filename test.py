import os
import json
from recordboy import RecordBoy
from pynput import mouse, keyboard


def test_init():
    print("Testing init...")

    recordboy = RecordBoy(path="test_events.json")
    assert recordboy.get_path() == "test_events.json"

    print("Init test passed.")


def test_getter_setter():
    print("Testing getter and setter...")

    recordboy = RecordBoy(path="test_events.json")
    recordboy.set_path("new_events.json")
    assert recordboy.get_path() == "new_events.json"

    print("Getter and setter test passed.")


def test_events():
    print("Testing mouse and keyboard events...")

    recordboy = RecordBoy(path="test_events.json")
    key = keyboard.Key.space

    recordboy.on_move(100, 200)
    recordboy.on_click(100, 200, mouse.Button.left, True)
    recordboy.on_scroll(100, 200, 0, -1)
    recordboy.on_press(key)
    recordboy.on_release(key)
    assert len(recordboy.events) == 5

    print("Event tests passed")


def test_record_store():
    print("Testing record...")

    recordboy = RecordBoy(path="test_events.json")
    recordboy.record()
    assert len(recordboy.events) > 0

    print("Record test passed.")

    assert os.path.exists("test_events.json")

    print("Store test passed.")


if __name__ == "__main__":
    print("Running tests...")
    test_init()
    test_getter_setter()
    test_events()
    test_record_store()
