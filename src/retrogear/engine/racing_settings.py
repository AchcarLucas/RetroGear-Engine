from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RacingSettings():
    DEPTH_FACTOR = 0.02

    PERSPECTIVE_OFFSET = 10.0
    PERSPECTIVE_RATIO = 0.25

    MAX_VISIBLE_DISTANCE = env.SCREEN_HEIGHT // 2

    BETWEEN_LINE = 1

    LANE_BORDER_RATIO = 0.07
    LANE_BORDER_HEIGHT = 15

    LANE_CENTER_RATIO = 0.02
    LANE_CENTER_HEIGHT = 15
