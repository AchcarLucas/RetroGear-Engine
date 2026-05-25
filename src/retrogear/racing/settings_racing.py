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

    SPEED_TEST = 100.0

    MAX_VISIBLE_SLICE_Z = env.SCREEN_HEIGHT // 2

    BETWEEN_LINE = 2.0

    LANE_BORDER_FACTOR = 60.0
    LANE_BORDER_RATIO = 0.04

    LANE_CENTER_FACTOR = 120.0
    LANE_CENTER_RATIO = 0.01
