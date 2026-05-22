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
             relative_z:float = 0.0,
             absolute_z:float = 0.0
        ):
        self._left_road = left_road
        self._right_road = right_road
        self._center_road = (left_road + right_road) / 2
        self._relative_z = relative_z
        self._absolute_z = absolute_z

    @property
    def left_road(self):
        return self._left_road
    
    @property
    def right_road(self):
        return self._right_road
    
    @property
    def relative_z(self):
        return self._relative_z
    
    @property
    def absolute_z(self):
        return self._absolute_z
    
    @property
    def road_width(self):
        return self._right_road - self._left_road