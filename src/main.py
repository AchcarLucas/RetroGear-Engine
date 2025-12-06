from src.manager.env_manager import EnvManager
from src.manager.logging_manager import LoggingManager
from src.manager.locator_manager import LocatorManager

from dotenv import load_dotenv

load_dotenv()

# configuration manager
env = EnvManager()

# logging manager
logging = LoggingManager().make_logger(env.LOGGEING_CONFIG_JSON)

# location manager
locator = LocatorManager()

# setting do env e do logging dentro do locator
locator.add_locator('env', env)
locator.add_locator('logging', logging)

if __name__ == "__main__":
    logging.info("POC - RetroGear")