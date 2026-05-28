from __future__ import annotations

from src.manager.locator_manager import LocatorManager
from src.retrogear.utils.color_palette import ColorPalette
from src.retrogear.utils.math_tools import MathTools

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class SegmentColorsRacing():
    def __init__(
        self,
        glass_color_a: tuple = ColorPalette.GRASS_A,
        glass_color_b: tuple = ColorPalette.GRASS_B,
        road_color_a: tuple = ColorPalette.ROAD_BRIGHT,
        road_color_b: tuple = ColorPalette.ROAD_DARK,
        lane_border_color_a:tuple = ColorPalette.LANE_BORDER_A,
        lane_border_color_b:tuple = ColorPalette.LANE_BORDER_B
    ):
        self.glass_color_a = glass_color_a
        self.glass_color_b = glass_color_b
        self.road_color_a = road_color_a
        self.road_color_b = road_color_b
        self.lane_border_color_a = lane_border_color_a
        self.lane_border_color_b = lane_border_color_b

    @classmethod
    def avarage(cls,
                parent_a: SegmentColorsRacing,
                parent_b: SegmentColorsRacing
        ):
        return cls(
            MathTools.avarage_tuple(parent_a.glass_color_a, parent_b.glass_color_a),
            MathTools.avarage_tuple(parent_a.glass_color_b, parent_b.glass_color_b),
            MathTools.avarage_tuple(parent_a.road_color_a, parent_b.road_color_a),
            MathTools.avarage_tuple(parent_a.road_color_b, parent_b.road_color_b),
            MathTools.avarage_tuple(parent_a.lane_border_color_a, parent_b.lane_border_color_a),
            MathTools.avarage_tuple(parent_a.lane_border_color_b, parent_b.lane_border_color_b),
        )