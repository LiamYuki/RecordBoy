import json
from pynput import mouse, keyboard


class RecordBoy:

    def __init__(self, path: str):
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
        pass

    def playback(self) -> None:
        pass

    # Listeners for mouse and keyboard events
    def on_move(self, x, y):
        """Mouse movement event.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
        """
        self.events.append(("move", x, y))

    def on_click(self, x, y, button, pressed):
        """Mouse click event.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            button (Button): The button that was clicked.
            pressed (bool): Whether the button was pressed or released.
        """
        self.events.append(("click", x, y, button.name, pressed))

    def on_scroll(self, x, y, dx, dy):
        """Mouse scroll event.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            dx (int): The amount scrolled in the x-direction.
            dy (int): The amount scrolled in the y-direction.
        """
        self.events.append(("scroll", x, y, dx, dy))

    def on_press(self, key):
        """Key press event.

        Args:
            key (keyboard.key): Key pressed.
        """
        try:
            self.events.append(("key_press", key.char))
        except AttributeError:
            self.events.append(("key_press", str(key)))

    def on_release(self, key):
        """Key release event.

        Args:
            key (keyboard.key): Key released.
        """
        self.events.append(("key_release", str(key)))

        # Esc stops listeners
        if key == keyboard.Key.esc:
            return False
