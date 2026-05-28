from src.retrogear.utils.math_tools import MathTools

from typing import List

from src.retrogear.racing.segment_racing import SegmentRacing, SubSegmentRacing

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class TrackRacing():
    def __init__(self):
        """
            - 'racing_segment' refers to the node segments of the track
            - 'racing_track' refers to the full segments of the track, including the sub-segments between the node segments
        """
        self.segments_racing = []
        self.subsegments_racing = []

    def append(self, segment_racing: SegmentRacing):
        self.segments_racing.append(segment_racing)
        for _ in range(segment_racing.racing_length * env.DISTANCE_PER_LENGTH):
            self.subsegments_racing.append(SubSegmentRacing.from_parent(segment_racing))

    def get_list_racing_segments(self) -> List[SegmentRacing]:
        return self.segments_racing
    
    def get_list_racing_subsegments(self) -> List[SubSegmentRacing]:
        return self.subsegments_racing
    
    def get_racing_sub_segment(self, distance) -> SubSegmentRacing:
        return self.subsegments_racing[MathTools.floor(distance) % len(self.subsegments_racing)]
    
    def get_max_distance(self) -> int:
        return len(self.subsegments_racing)

    def __repr__(self):
        text = "Racing Segment:\n"
        for i, segment in enumerate(self.segments_racing):
            text += \
            f" - segment {i:06.0f}: \t \
            length={segment.racing_length:06.0f}, \t \
            width_factor={segment.racing_width_factor:05.3f}, \
            curve_factor={segment.racing_curve_factor:05.3f}, \
            elevation_factor={segment.racing_elevation_factor:05.3f}\n"

        distance = 0

        text += "Racing SubSegment:\n"
        for i, subsegment in enumerate(self.subsegments_racing):
            text += \
            f" - subsegment {i:06.0f}: \t \
            distance={distance:04.0f}, \t \
            length={subsegment.racing_length:04.0f}, \t \
            width_factor={subsegment.racing_width_factor:05.3f}, \
            curve_factor={subsegment.racing_curve_factor:05.3f}, \
            elevation_factor={subsegment.racing_elevation_factor:05.3f}\n"

            distance += 1

        return text