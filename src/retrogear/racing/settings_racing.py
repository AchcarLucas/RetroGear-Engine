from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class SettingsRacing():
    DEPTH_FACTOR = 0.012
    DEPTH_SLICE_FACTOR = 2.0

    PERSPECTIVE_OFFSET = 20.0
    PERSPECTIVE_FACTOR = 0.42

    MAX_VISIBLE_SLICE_Z = env.SCREEN_HEIGHT // 2

    MULTILANE_FACTOR = 0.75

    LANE_BORDER_STRIBE_FACTOR = 60.0
    LANE_BORDER_WIDTH_FACTOR = 0.025

    LANE_TRACK_STRIBE_FACTOR = 120.0
    LANE_TRACK_WIDTH_FACTOR = 0.015

    SPEED_TEST = 40.0
