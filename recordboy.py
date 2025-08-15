import json
from pynput import mouse, keyboard


class RecordBoy:

    def __init__(self, path: str):
        """Initialize the RecordBoy instance.

        Args:
            path (str): The file path for the recorded events.
        """
        self.path = path

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
