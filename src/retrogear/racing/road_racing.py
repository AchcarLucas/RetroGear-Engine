from typing import Self, List

from src.manager.locator_manager import LocatorManager
from src.retrogear.utils.math_tools import MathTools

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RoadRacing():
    def __init__(self,
             left_road,
             right_road,
             slice_z : float = 0.0,
             relative_z:float = 0.0,
             absolute_z:float = 0.0,
             relative_t:float = 0.0,
             width_factor:float = 1.0
        ):
        self._left_road = left_road
        self._right_road = right_road
        self._center_road = (left_road + right_road) / 2
        self._slice_z = slice_z
        self._relative_z = relative_z
        self._absolute_z = absolute_z
        self._relative_t = relative_t
        self._width_factor = width_factor

    @property
    def left_road(self):
        return self._left_road
    
    @property
    def right_road(self):
        return self._right_road
    
    @property
    def center_road(self):
        return self._center_road
    
    @property
    def slice_z(self):
        return self._slice_z

    @property
    def relative_z(self):
        return self._relative_z
    
    @property
    def absolute_z(self):
        return self._absolute_z
    
    @property
    def relative_t(self):
        return self._relative_t
    
    @property
    def width_factor(self):
        return self._width_factor
    
    @property
    def road_width(self):
        return self._right_road - self._left_road