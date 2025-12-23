"""
Docstring for render_racing
"""

import pygame

from src.retrogear.interface.render_interface import IRender

from src.retrogear.engine.racing_track import RacingTrack
from src.retrogear.engine.racing_settings import RacingSettings
from src.retrogear.engine.racing_road import RacingRoad

from src.retrogear.utils.color_palette import ColorPalette

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RacingRenderer(IRender):
    def __init__(self, racing_track: RacingTrack=None):
        self.racing_track = racing_track

        self.time = 0

        self.camera_distance = 0
        self.camera_offset =  0

        self.center_screen_x = env.SCREEN_WIDTH // 2
        self.center_screen_y = env.SCREEN_HEIGHT // 2

        self.depth = (self.center_screen_y / RacingSettings.MAX_VISIBLE_DISTANCE) * RacingSettings.DEPTH_FACTOR

    def set_racing_track(self,
                         racing_track: RacingTrack
        ):
        """
            Set the racing track to be rendered.
        """
        self.racing_track = racing_track

    def update(self, delta_time: float):
        """
        Update the renderer state.
        """
        self.camera_distance += delta_time * 100  # Example speed
        self.camera_distance = self.camera_distance % self.racing_track.get_max_distance()

        self.time += delta_time

    def event(self, event):
        """
            Handle events.
        """
        pass

    def perspective(
            self, 
            segment: RacingTrack,
            distance: float
        ) -> RacingRoad:
        perspective = self.depth * (distance + RacingSettings.PERSPECTIVE_OFFSET)
        inverse_perspective = 1.0 / perspective

        screen_x = self.center_screen_x + (segment.racing_curve_factor * inverse_perspective)
        screen_y = self.center_screen_y + (segment.racing_elevation_factor * inverse_perspective)

        road_width = (env.SCREEN_WIDTH * RacingSettings.ROAD_FACTOR) * perspective

        y = (RacingSettings.BETWEEN_LINE * distance) + screen_y

        left_road = int(screen_x - road_width) + self.camera_offset
        right_road = int(screen_x + road_width) + self.camera_offset

        return RacingRoad(left_road, right_road, y)

    def render(self, screen):
        """
            Render the racing track.
        """
        if self.racing_track is None:
            return
        
        screen.fill(ColorPalette.SKY)

        # Render the road
        for visable_distance in range(0, RacingSettings.MAX_VISIBLE_DISTANCE - 1):
            current_distance = visable_distance + self.camera_distance

            segment_a = self.racing_track.get_racing_sub_segment(distance=current_distance)
            segment_b = self.racing_track.get_racing_sub_segment(distance=current_distance + 1)

            road_a: RacingRoad = self.perspective(segment_a, visable_distance)
            road_b: RacingRoad = self.perspective(segment_b, visable_distance + 1)

            points = [
                (road_a.left_road, road_a.y),
                (road_a.right_road, road_a.y),
                (road_b.right_road, road_b.y),
                (road_b.left_road, road_b.y)
            ]

            pygame.draw.polygon(screen, ColorPalette.ROAD, points)

    def render_road(self,
                    screen,
                    road_a: RacingRoad,
                    road_b: RacingRoad
        ):
        pass

    def render_border(self,
                      screen,
                      road_a: RacingRoad,
                      road_b: RacingRoad
        ):
        pass
