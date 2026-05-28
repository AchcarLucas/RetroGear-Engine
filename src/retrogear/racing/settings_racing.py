from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class SettingsRacing():
    DEPTH_FACTOR = 0.012

    PERSPECTIVE_OFFSET = 20.0
    PERSPECTIVE_RATIO = 0.42

    MAX_VISIBLE_SLICE_Z = env.SCREEN_HEIGHT // 2

    BETWEEN_LINE = 2.0

    LANE_BORDER_FACTOR = 60.0
    LANE_BORDER_RATIO = 0.04

    LANE_TRACK_FACTOR = 120.0
    LANE_TRACK_RATIO = 0.01

    LANE_RANGE_FACTOR = 0.75

    SPEED_TEST = 35.0
