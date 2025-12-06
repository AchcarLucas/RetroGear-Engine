#################################################
from dotenv import load_dotenv

load_dotenv()

#################################################

from src.manager.locator_manager import LocatorManager
from src.manager.logging_manager import LoggingManager
from src.manager.env_manager import EnvManager

# create configuration manager
env = EnvManager()

# create logging manager
logging = LoggingManager().make_logger(env.LOGGEING_CONFIG_JSON)

# create location manager
locator = LocatorManager()

# setting instances to locator
locator.add_locator('env', env)
locator.add_locator('logging', logging)

#################################################

from src.retrogear.engine.retrogear_engine import RetroGearEngine

if __name__ == "__main__":
    logging.info("RetroGear - Engine (POC)")

    engine = RetroGearEngine(
        env.CAPTION,
        env.SCREEN_WIDTH,
        env.SCREEN_HEIGHT,
        env.FPS
    )

    engine.run()