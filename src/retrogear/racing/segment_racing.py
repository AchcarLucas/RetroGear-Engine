from typing import Self, List

from src.retrogear.utils.math_tools import MathTools
from src.manager.locator_manager import LocatorManager

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
                 racing_elevation_factor : float
        ):
        self.racing_length = racing_length
        self.racing_width_factor = racing_width_factor
        self.racing_curve_factor = racing_curve_factor
        self.racing_elevation_factor = racing_elevation_factor

    def interpolate(self, next: Self) -> List["SubSegmentRacing"]:
        """
            Interpolates the current segment with the next segment, creating sub-segments between them.

            next: the next segment to be interpolated

            Returns a list of interpolated SubSegmentRacing objects.
        """
        sub_racing_segment_interpolated: List["SubSegmentRacing"] = []

        for i in range(0, self.racing_length):
            sub_racing_segment = SubSegmentRacing(
                racing_width_factor=self.racing_width_factor,
                racing_curve_factor=self.racing_curve_factor,
                racing_elevation_factor=self.racing_elevation_factor
            )

            sub_racing_segment_interpolated.append(sub_racing_segment)

        return sub_racing_segment_interpolated

"""
    The SubSegmentRacing class is simply an alias of SegmentRacing.
    Its behavior is identical to SegmentRacing, but it is used to distinguish full segments from node segments.
"""
class SubSegmentRacing(SegmentRacing):
    def __init__(self,
                 racing_width_factor : float,
                 racing_curve_factor : float,
                 racing_elevation_factor : float
        ):
        super().__init__(racing_length=1,
                         racing_width_factor=racing_width_factor,
                         racing_curve_factor=racing_curve_factor,
                         racing_elevation_factor=racing_elevation_factor
        )

    @classmethod
    def from_parent(cls, parent: SegmentRacing):
        return cls(
            racing_width_factor=parent.racing_width_factor,
            racing_curve_factor=parent.racing_curve_factor,
            racing_elevation_factor=parent.racing_elevation_factor
        )