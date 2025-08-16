import json
import os
import time
import pyautogui
import logging
from pynput import mouse, keyboard


class RecordBoy:

    def __setup_logging(self) -> None:
        """Set up logging for the RecordBoy instance."""
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("recordboy.log"), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def __init__(self, path: str) -> None:
        """Initialize the RecordBoy instance.

        Args:
            path (str): The file path for the recorded events.
        """
        self.path = path
        self.events = []
        self.recording = False
        self.playing = False
        self.__setup_logging()

        self.logger.debug("RecordBoy initialized")

    def get_path(self) -> str:
        """Get the current file path.

        Returns:
            str: The current file path.
        """
        self.logger.debug(f"Getting path: {self.path}")
        return self.path

    def set_path(self, path: str) -> None:
        """Set the file path.

        Args:
            path (str): The file path for the recorded video or events.
        """
        self.logger.debug(f"Setting path from {self.path} to {path}")
        self.path = path

    def record(self) -> None:
        """Start recording mouse and keyboard events."""
        # Wait for start command
        self.start_recording()

        if self.recording:
            self.logger.info("Recording started")
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
            self.logger.info("Recording stopped")

            # Store events in file
            try:
                self.store()
                self.logger.info(f"Events stored in {self.path}")
            except Exception as e:
                self.logger.error(f"Error storing events: {e}")
                raise e

    def playback(self) -> None:
        """Play back recorded mouse and keyboard events.

        Raises:
            FileNotFoundError: If the events file does not exist.
        """

        # Load recorded events
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.events = json.load(f)

            self.logger.info(f"Loaded events from {self.path}")
        else:
            self.logger.error(f"No such file: {self.path}")
            raise FileNotFoundError(f"No such file: {self.path}")
        # Give time to switch windows
        time.sleep(3)

        # Wait for start playback command
        self.start_playing()

        self.logger.info(f"Starting playback from {self.path}")
        if self.playing:
            self.logger.info("Playback started")

            # Start playback
            for event in self.events:
                event_type = event[0]
                if event_type == "move":
                    x, y = event[1], event[2]
                    pyautogui.moveTo(x, y)
                elif event_type == "click":
                    x, y, button, pressed = event[1], event[2], event[3], event[4]

                    if pressed:
                        pyautogui.click(x, y, button=button)
                elif event_type == "scroll":
                    dy = event[4]
                    pyautogui.scroll(dy)
                elif event_type == "key_press":
                    key = event[1]
                    pyautogui.press(key)

            self.logger.info("Playback finished")

    def store(self) -> None:
        """Store recorded events in a JSON file.

        Exceptions:
            Exception: If there is an error writing to the file.
        """
        try:
            with open(self.path, "w") as f:
                json.dump(self.events, f)
            self.logger.info(f"Events stored in {self.path}")
            self.logger.debug(f"Stored events: {self.events}")
        except Exception as e:
            self.logger.error(f"Error storing events: {e}")
            raise e

    def start_recording(self) -> None:
        """Start recording mouse and keyboard events."""
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        keyboard_listener.start()
        self.logger.debug("Waiting for start key...")

        # Start key was pressed
        keyboard_listener.join()
        self.logger.debug("Start key pressed, recording...")
        self.recording = True

    def start_playing(self) -> None:
        """Start playing back recorded mouse and keyboard events."""
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        keyboard_listener.start()
        self.logger.debug("Waiting for start key...")

        # Start key was pressed
        keyboard_listener.join()
        self.logger.debug("Start key pressed, recording...")
        self.playing = True

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
        if self.recording:
            try:
                self.events.append(("key_press", key.char))
            except AttributeError:
                self.events.append(("key_press", str(key)))

    def on_release(self, key) -> bool:
        """Key release event.

        Args:
            key (keyboard.key): Key released.
        """
        if self.recording:
            self.events.append(("key_release", str(key)))

        # ESC key starts/stops listeners
        if key == keyboard.Key.esc and not self.recording:
            self.logger.info("Starting to record mouse and keyboard events...")
            return False

        if key == keyboard.Key.esc and self.recording:
            self.logger.info("Stopping recording...")
            return False
