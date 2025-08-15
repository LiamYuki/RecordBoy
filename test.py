from recordboy import RecordBoy


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


if __name__ == "__main__":
    print("Running tests...")
    test_init()
    test_getter_setter()
