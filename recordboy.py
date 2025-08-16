import json
from pynput import mouse, keyboard


class RecordBoy:

    def __init__(self, path: str) -> None:
        """Initialize the RecordBoy instance.

        Args:
            path (str): The file path for the recorded events.
        """
        self.path = path
        self.events = []

    def get_path(self) -> str:
        """Get the current file path.

        Returns:
            str: The current file path.
        """
        return self.path

    def set_path(self, path: str) -> None:
        """Set the file path.

        Args:
            path (str): The file path for the recorded video or events.
        """
        self.path = path

    def record(self) -> None:
        """Start recording mouse and keyboard events."""
        # Start listeners
        mouse_listener = mouse.Listener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        )
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

        keyboard_listener.start()
        mouse_listener.start()

        # Esc key pressed
        keyboard_listener.join()
        mouse_listener.stop()

        # Store events in file
        try:
            self.store()
            print(f"Events stored in {self.path}")
        except Exception as e:
            print(f"Error storing events: {e}")

    def playback(self) -> None:
        pass

    def store(self) -> None:
        """Store recorded events in a JSON file.

        Exceptions:
            Exception: If there is an error writing to the file.
        """
        try:
            with open(self.path, "w") as f:
                json.dump(self.events, f)
        except Exception as e:
            raise e

    # Mouse and keyboard events
    def on_move(self, x, y) -> None:
        """Mouse movement event.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
        """
        self.events.append(("move", x, y))

    def on_click(self, x, y, button, pressed) -> None:
        """Mouse click event.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            button (Button): The button that was clicked.
            pressed (bool): Whether the button was pressed or released.
        """
        self.events.append(("click", x, y, button.name, pressed))

        # Stop listener
        if not pressed:
            return False

    def on_scroll(self, x, y, dx, dy) -> None:
        """Mouse scroll event.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            dx (int): The amount scrolled in the x-direction.
            dy (int): The amount scrolled in the y-direction.
        """
        self.events.append(("scroll", x, y, dx, dy))

    def on_press(self, key) -> None:
        """Key press event.

        Args:
            key (keyboard.key): Key pressed.

        Exceptions:
          AttributeError: If the key does not have a char attribute.
        """
        try:
            self.events.append(("key_press", key.char))
        except AttributeError:
            self.events.append(("key_press", str(key)))

    def on_release(self, key) -> bool:
        """Key release event.

        Args:
            key (keyboard.key): Key released.
        """
        self.events.append(("key_release", str(key)))

        # ESC key stops listeners
        if key == keyboard.Key.esc:
            return False
