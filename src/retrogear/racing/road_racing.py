from typing import Self, List

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RoadRacing():
    def __init__(self,
             left_road,
             right_road,
             y    
        ):
        self._left_road = left_road
        self._right_road = right_road
        self._y = y

    @property
    def left_road(self):
        return self._left_road
    
    @property
    def right_road(self):
        return self._right_road
    
    @property
    def y(self):
        return self._y
    
    @property
    def road_width(self):
        return self._right_road - self._left_road