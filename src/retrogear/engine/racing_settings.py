from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RacingSettings():
    DEPTH_FACTOR = 0.02
    PERSPECTIVE_OFFSET = 4.0

    ROAD_FACTOR = 0.2

    BETWEEN_LINE = 1

    MAX_VISIBLE_DISTANCE = env.SCREEN_HEIGHT // 2

    BORDER_FACTOR = 0.1
