from src.manager.locator_manager import LocatorManager

from src.retrogear.racing.segment_colors_racing import SegmentColorsRacing
from src.retrogear.racing.segment_objects_racing import SegmentObjectsRacing

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class SegmentRacing():
    def __init__(self,
                 racing_length : int,
                 racing_width_factor : float,
                 racing_curve_factor : float,
                 racing_elevation_factor : float,
                 racing_colors : SegmentColorsRacing = SegmentColorsRacing(),
                 racing_objects : SegmentObjectsRacing = SegmentObjectsRacing()
        ):
        self.racing_length = racing_length
        self.racing_width_factor = racing_width_factor
        self.racing_curve_factor = racing_curve_factor
        self.racing_elevation_factor = racing_elevation_factor
        self.racing_colors = racing_colors
        self.racing_objects = racing_objects

"""
    The SubSegmentRacing class is simply an alias of SegmentRacing.
    Its behavior is identical to SegmentRacing, but it is used to distinguish full segments from node segments.
"""
class SubSegmentRacing(SegmentRacing):
    def __init__(self,
                 racing_width_factor : float,
                 racing_curve_factor : float,
                 racing_elevation_factor : float,
                 racing_colors:SegmentColorsRacing,
                 racing_objects:SegmentObjectsRacing
        ):
        super().__init__(racing_length=1,
                         racing_width_factor=racing_width_factor,
                         racing_curve_factor=racing_curve_factor,
                         racing_elevation_factor=racing_elevation_factor,
                         racing_colors=racing_colors,
                         racing_objects=racing_objects
        )

    @classmethod
    def from_parent(cls, parent: SegmentRacing):
        return cls(
            racing_width_factor=parent.racing_width_factor,
            racing_curve_factor=parent.racing_curve_factor,
            racing_elevation_factor=parent.racing_elevation_factor,
            racing_colors=parent.racing_colors,
            racing_objects=parent.racing_objects
        )