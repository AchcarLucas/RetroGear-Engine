import os

from src.utils.singleton_meta import SingletonMeta

class EnvManager(metaclass=SingletonMeta):
    def __init__(self):
        # name project
        self.CAPTION = self.get_env("CAPTION", "RetroGame - Engine")

        # debug mode
        self.DEBUG_MODE = str(self.get_env('DEBUG_MODE', False)).lower() == "true"

        # logger config json
        self.LOGGEING_CONFIG_JSON = self.get_env('LOGGEING_CONFIG_JSON', "./src/json/logging/logging_config_default.json")

        # retrogear config
        self.SCREEN_WIDTH = int(self.get_env("SCREEN_WIDTH", 800))
        self.SCREEN_HEIGHT = int(self.get_env("SCREEN_HEIGHT", 600))

        self.FPS = int(self.get_env("FPS", 60))

        self.DISTANCE_PER_LENGTH = int(self.get_env("DISTANCE_PER_LENGTH", 2))

    def get_env(self, key, otherwise=None):
        return os.getenv(key, otherwise)
    
    def set_env(self, key, value):
        os.environ[key] = value