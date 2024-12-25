import json
import os
import sys

class SettingsManager:
    def __init__(self, file_path=None):
        self.default_settings = {
            "download_location": "",
            "theme": "light"
        }
        if file_path is None:
            if getattr(sys, 'frozen', False):  
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)
            file_path = os.path.join(base_path, "settings.json")
        self.file_path = file_path
        self.settings = self.default_settings.copy()
        self.load_settings()

    def load_settings(self):
        """Loads settings from the JSON file, or initializes with defaults if the file doesn't exist."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    self.settings = json.load(file)
            except (json.JSONDecodeError, IOError):
                print("Error loading settings. Reverting to default settings.")
                self.settings = self.default_settings.copy()
        else:
            self.save_settings()

    def save_settings(self):
        """Saves the current settings to the JSON file."""
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.settings, file, indent=4)
        except IOError:
            print("Error saving settings.")

    def get(self, key, default=None):
        """Gets a setting value."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Sets a setting value and saves the changes."""
        self.settings[key] = value
        self.save_settings()
