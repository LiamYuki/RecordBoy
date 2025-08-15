class RecordBoy:
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
