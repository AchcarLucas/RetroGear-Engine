from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class SettingsRacing():
    DEPTH_FACTOR = 0.01

    CAMERA_HEIGHT = 150.0

    ROAD_WIDTH_PERSPECTIVE = 0.42

    MAX_VISIBLE_SLICE_Z = env.SCREEN_HEIGHT // 2

    MULTILANE_FACTOR = 0.75

    LANE_BORDER_STRIBE_FACTOR = 60.0
    LANE_BORDER_WIDTH_FACTOR = 0.025

    LANE_TRACK_STRIBE_FACTOR = 120.0
    LANE_TRACK_WIDTH_FACTOR = 0.015

    SPEED_TEST = 20.0
