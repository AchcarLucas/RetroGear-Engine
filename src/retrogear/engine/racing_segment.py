from typing import Self, List

from src.retrogear.utils.interpolator_tools import InterpolatorTools
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
            Interpola o segmento atual com o próximo segmento, criando sub-segmentos entre eles.
            - next: próximo segmento a ser interpolado

            Retorna uma lista de SubRacingSegment interpolados
        """
        sub_racing_segment_interpolated: List["SubRacingSegment"] = []

        for i in range(1, self.racing_length):
            t = i / (self.racing_length)
            racing_width_factor = InterpolatorTools.lerp(self.racing_width_factor, next.racing_width_factor, t)
            racing_curve_factor = InterpolatorTools.lerp(self.racing_curve_factor, next.racing_curve_factor, t)
            racing_elevation_factor = InterpolatorTools.lerp(self.racing_elevation_factor, next.racing_elevation_factor, t)

            sub_racing_segment = SubRacingSegment(
                racing_width_factor=racing_width_factor,
                racing_curve_factor=racing_curve_factor,
                racing_elevation_factor=racing_elevation_factor
            )

            sub_racing_segment_interpolated.append(sub_racing_segment)

        return sub_racing_segment_interpolated

"""
    Classe 'SubRacingSegment' é apenas uma classe alias da 'RacingSegment', seu comportamento 
    é idêntico ao 'RacingSegment', mas é usada para diferenciar os segmentos completos dos segmentos nodes
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