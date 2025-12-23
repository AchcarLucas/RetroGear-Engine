from typing import Self, List

from src.retrogear.utils.math_tools import MathTools
from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RacingSegment():
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

    def interpolate(self, next: Self) -> List["SubRacingSegment"]:
        """
            Interpolates the current segment with the next segment, creating sub-segments between them.

            next: the next segment to be interpolated

            Returns a list of interpolated SubRacingSegment objects.
        """
        sub_racing_segment_interpolated: List["SubRacingSegment"] = []

        for i in range(1, self.racing_length):
            t = i / (self.racing_length)
            racing_width_factor = MathTools.lerp(self.racing_width_factor, next.racing_width_factor, t)
            racing_curve_factor = MathTools.lerp(self.racing_curve_factor, next.racing_curve_factor, t)
            racing_elevation_factor = MathTools.lerp(self.racing_elevation_factor, next.racing_elevation_factor, t)

            sub_racing_segment = SubRacingSegment(
                racing_width_factor=racing_width_factor,
                racing_curve_factor=racing_curve_factor,
                racing_elevation_factor=racing_elevation_factor
            )

            sub_racing_segment_interpolated.append(sub_racing_segment)

        return sub_racing_segment_interpolated

"""
    The SubRacingSegment class is simply an alias of RacingSegment.
    Its behavior is identical to RacingSegment, but it is used to distinguish full segments from node segments.
"""
class SubRacingSegment(RacingSegment):
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
    def from_parent(cls, parent: RacingSegment):
        return cls(
            racing_width_factor=parent.racing_width_factor,
            racing_curve_factor=parent.racing_curve_factor,
            racing_elevation_factor=parent.racing_elevation_factor
        )