import cv2
import numpy as np
import mss
import time
import threading
from pynput import mouse, keyboard


class RecordBoy:

    def __init__(self, config: dict = None, path: str = None):
        """Initialize configuration settings.

        Args:
            config (dict): The configuration dictionary.
            path (str): The file path for the recorded video or events.

        Configuration dictionary should contain:
        - video_file: <string> Name of the video file to record (avi)
        - events_file: <string> Name of the events file for mouse and keyboard event playback (txt)
        - fps: <int> Frames per second for video recording
        - screen: {<string>: <int>} Dictionary containing screen dimensions (top, left, width, height)
        """
        # Can't record or playback without a config or path so exception is thrown
        if not config:
            self.path = path
        elif self._validate_config(config):
            self.config = config
            self.events = []
            self.timer = None
            self.path = None
        else:
            raise ValueError("Invalid configuration or path.")

    def get_config(self) -> dict:
        """Get the current configuration.

        Returns:
            dict: The current configuration dictionary.
        """
        return self.config

    def get_path(self) -> str:
        """Get the current file path.

        Returns:
            str: The current file path.
        """
        return self.path

    def set_config(self, config: dict) -> None:
        """Set the configuration.

        Args:
            config (dict): The configuration dictionary.
        """
        if self._validate_config(config):
            self.config = config
        else:
            raise ValueError("Invalid configuration.")

    def set_path(self, path: str) -> None:
        """Set the file path.

        Args:
            path (str): The file path for the recorded video or events.
        """
        self.path = path

    def record(self) -> None:
        # Start timer for listeners
        self.timer = time.time()

    def _validate_config(self, config: dict) -> bool:
        """Validate the configuration dictionary.

        Args:
            config (dict): The configuration dictionary to validate.

        Returns:
            bool: True if valid false otherwise.
        """
        for key in ["video_file", "events_file", "fps", "screen"]:
            if key not in config:
                return False
        return True

    # Listeners for mouse and keyboard
    def _on_move(self, x, y):
        """Handle mouse movement events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
        """
        self.events.append(("move", time.time() - self.timer, x, y))

    def _on_click(self, x, y, button, pressed):
        """Handle mouse click events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            button (Button): The button that was clicked.
            pressed (bool): True if the button was pressed, False if released.
        """
        self.events.append(
            ("click", time.time() - self.timer, x, y, button.name, pressed)
        )

    def _on_scroll(self, x, y, dx, dy):
        """Handle mouse scroll events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            dx (float): The horizontal scroll amount.
            dy (float): The vertical scroll amount.
        """
        self.events.append(("scroll", time.time() - self.timer, x, y, dx, dy))

    def _on_press(self, key):
        """Handle keyboard press events.

        Args:
            key (Key): The key that was pressed.
        """
        try:
            self.events.append(("key_press", time.time() - self.timer, key.char))
        except AttributeError as e:
            self.events.append(("key_press", time.time() - self.timer, str(key)))

    def _on_release(self, key) -> bool:
        """Handle keyboard release events.

        Args:
            key (Key): The key that was released.

        Returns:
            bool: False if the ESC key was released, True otherwise.
        """
        self.events.append(("key_release", time.time() - self.timer, str(key)))

        if key == keyboard.Key.esc:
            # Stop listeners
            return False
