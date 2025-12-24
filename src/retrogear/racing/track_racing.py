import math

from typing import List

from src.retrogear.racing.segment_racing import SegmentRacing, SubSegmentRacing

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class TrackRacing():
    def __init__(self, 
                 racing_segments: List[SegmentRacing] = None,
        ):
        """
            - 'racing_segment' refers to the node segments of the track
            - 'racing_track' refers to the full segments of the track, including the sub-segments between the node segments
        """
        self.racing_segments = [] if racing_segments is None else racing_segments

        self.racing_track: List[SubSegmentRacing] = []

    def add_racing_segment(self, racing_segment: SegmentRacing):
        self.racing_segments.append(racing_segment)

    def get_racing_segments(self) -> List[SegmentRacing]: 
        return self.racing_segments
    
    def get_racing_sub_segment(self, distance) -> SubSegmentRacing:
        return self.racing_track[math.floor(distance / env.DISTANCE_PER_LENGTH) % len(self.racing_track)]

    def get_racing_track(self) -> List[SubSegmentRacing]:
        return self.racing_track
    
    def get_max_distance(self) -> int:
        return len(self.racing_track) * env.DISTANCE_PER_LENGTH

    def generate_racing_track(self):
        """
            Method to generate the complete track with interpolated sub-segments.
        """
        self.racing_track: List[SubSegmentRacing] = []

        for i in range(len(self.racing_segments) - 1):
            # obtem o segmento atual
            current_segment = self.racing_segments[i]
            # obtem o proximo segmento
            next_segment = self.racing_segments[i + 1]

            # adiciona o segmento atual no tracking da pista 
            # cria uma cópia do SegmentRacing do segmento atual como SubSegmentRacing
            self.racing_track.append(SubSegmentRacing.from_parent(current_segment))

            # gera os subsegmentos entre o segmento atual e o proximo
            sub_racing_segment_interpolated = current_segment.interpolate(next_segment)

            # adiciona os subsegmentos no tracking da pista
            self.racing_track.extend(sub_racing_segment_interpolated)

        # adiciona o ultimo segmento no tracking da pista para fechar o percurso
        self.racing_track.append(SubSegmentRacing.from_parent(self.racing_segments[-1]))

    def __repr__(self):
        text = "Racing Segment:\n"
        for i, segment in enumerate(self.racing_segments):
            text += \
            f" - segment {i:06.0f}: \t \
            length={segment.racing_length:06.0f}, \t \
            width_factor={segment.racing_width_factor:05.3f}, \
            curve_factor={segment.racing_curve_factor:05.3f}, \
            elevation_factor={segment.racing_elevation_factor:05.3f}\n"

        distance = 0

        text += "Racing Track:\n"
        for i, subsegment in enumerate(self.racing_track):
            text += \
            f" - track {i:06.0f}: \t \
            distance={distance:04.0f}, \t \
            length={subsegment.racing_length:04.0f}, \t \
            width_factor={subsegment.racing_width_factor:05.3f}, \
            curve_factor={subsegment.racing_curve_factor:05.3f}, \
            elevation_factor={subsegment.racing_elevation_factor:05.3f}\n"

            distance += env.DISTANCE_PER_LENGTH

        return text