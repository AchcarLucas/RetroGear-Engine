"""
Docstring for render_racing
"""

import pygame

from src.retrogear.interface.render_interface import IRender

from src.retrogear.engine.racing_track import RacingTrack
from src.retrogear.engine.racing_settings import RacingSettings
from src.retrogear.engine.racing_road import RacingRoad

from src.retrogear.utils.color_palette import ColorPalette
from src.retrogear.utils.math_tools import MathTools

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
        #self.camera_distance -= delta_time * 100  # Example speed
        self.camera_distance = 450
        self.camera_distance = self.camera_distance % self.racing_track.get_max_distance()

        self.time += delta_time

    @property
    def minimum_y(self):
        return (RacingSettings.BETWEEN_LINE * RacingSettings.MAX_VISIBLE_DISTANCE) + self.center_screen_y

    @property
    def maximum_y(self):
        return self.center_screen_y

    def perspective(self, visable_distance: float):
        return self.depth * (visable_distance + RacingSettings.PERSPECTIVE_OFFSET)

    def project(
            self, 
            segment: RacingTrack,
            visable_distance: float
        ) -> RacingRoad:
        perspective = self.perspective(visable_distance)
        inverse_perspective = 1.0 / perspective

        screen_x = self.center_screen_x + (segment.racing_curve_factor * inverse_perspective)
        screen_y = self.center_screen_y + (segment.racing_elevation_factor * inverse_perspective)

        road_width = (env.SCREEN_WIDTH * RacingSettings.PERSPECTIVE_RATIO) * perspective

        y = (RacingSettings.BETWEEN_LINE * visable_distance) + screen_y

        left_road = int(screen_x - road_width) + self.camera_offset
        right_road = int(screen_x + road_width) + self.camera_offset

        return RacingRoad(left_road, right_road, y)

    def event(self, event):
        """
            Handle events.
        """
        pass

    def render(self, screen):
        """
            Render the racing track.
        """
        if self.racing_track is None:
            return
        
        screen.fill(ColorPalette.SKY)

        # center line
        pygame.draw.line(screen, (255, 255, 255), (0, self.center_screen_y), (env.SCREEN_WIDTH, self.center_screen_y))

        # Render the road
        for visable_distance in range(0, RacingSettings.MAX_VISIBLE_DISTANCE - 1):
            current_distance = visable_distance + self.camera_distance

            segment_a = self.racing_track.get_racing_sub_segment(distance=current_distance)
            segment_b = self.racing_track.get_racing_sub_segment(distance=current_distance + 1)

            road_a: RacingRoad = self.project(segment_a, visable_distance)
            road_b: RacingRoad = self.project(segment_b, visable_distance + 1)

            '''
            self.render_road(
                screen,
                visable_distance,
                current_distance,
                road_a,
                road_b
            )
            '''

            """
                TODO
                    Devo interpolar as linhas dos trapezios e não desenhar os trapezios,
                    assim, vou conseguir pintar a pista do jeito que quero
            """

            pygame.draw.line(screen, ColorPalette.ROAD, (road_a.left_road, road_a.y), (road_a.right_road, road_a.y))

            self.render_border(
                screen,
                visable_distance,
                current_distance,
                road_a,
                road_b
            )

    def render_road(self,
                    screen,
                    visable_distance: float,
                    current_distance: float,
                    road_a: RacingRoad,
                    road_b: RacingRoad
        ):
        points = [
            (road_a.left_road, road_a.y),
            (road_a.right_road, road_a.y),
            (road_b.right_road, road_b.y),
            (road_b.left_road, road_b.y)
        ]

        pygame.draw.polygon(screen, ColorPalette.ROAD, points)

    def render_border(self,
                      screen,
                      visable_distance: float,
                      current_distance: float,
                      road_a: RacingRoad,
                      road_b: RacingRoad
        ):
        road_factor_a = road_a.road_width * RacingSettings.LANE_BORDER_RATIO
        road_factor_b = road_b.road_width * RacingSettings.LANE_BORDER_RATIO

        perspective = self.perspective(visable_distance)
        inverse_perspective = 1 / perspective

        period = 50.0 / (inverse_perspective * 2.5)

        #logging.info(f"period: {period}")

        logging.info(f"road_a.y: {road_a.y} - road_b.y: {road_b.y}")

        wave = MathTools.rectangular_wave(visable_distance + self.center_screen_y, period, duty=0.5)

        #logging.info(visable_distance + self.center_screen_y)

        if wave:
            border_color = ColorPalette.LANE_BORDER_A
        else:
            border_color = ColorPalette.LANE_BORDER_B

        # Left Road
        pygame.draw.polygon(screen, border_color, [
            (road_a.left_road, road_a.y),
            (road_a.left_road + road_factor_a, road_a.y),
            (road_b.left_road + road_factor_b, road_b.y),
            (road_b.left_road, road_b.y)
        ])

        # Right Road
        pygame.draw.polygon(screen, border_color, [
            (road_a.right_road, road_a.y),
            (road_a.right_road + road_factor_a, road_a.y),
            (road_b.right_road + road_factor_b, road_b.y),
            (road_b.right_road, road_b.y)
        ])
