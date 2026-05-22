import pygame

from src.retrogear.interface.engine_interface import IEngine

from src.retrogear.racing.track_racing import TrackRacing
from src.retrogear.racing.segment_racing import SubSegmentRacing
from src.retrogear.racing.settings_racing import SettingsRacing
from src.retrogear.racing.road_racing import RoadRacing

from src.retrogear.utils.color_palette import ColorPalette
from src.retrogear.utils.math_tools import MathTools

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RacingEngine(IEngine):
    def __init__(self, racing_track: TrackRacing=None):
        self.racing_track = racing_track

        self.center_screen_x: int = env.SCREEN_WIDTH // 2
        self.center_screen_y: int = env.SCREEN_HEIGHT // 2

        self.depth: float = (self.center_screen_y / SettingsRacing.MAX_VISIBLE_DISTANCE) * SettingsRacing.DEPTH_FACTOR

        self.current_segment: SubSegmentRacing = None
        self.previous_segment: SubSegmentRacing = None

        self.laps: int = 0
        self.camera_distance: float = 0.0
        self.camera_offset: float = 0.0

        self.speed = SettingsRacing.SPEED_TEST

        self.curve_accumulator: float = 0.0
        self.elevator_accumulator: float = 0.0

    def set_racing_track(self,
                         racing_track: TrackRacing
        ):
        """
            Set the racing track to be rendered.
        """
        self.racing_track = racing_track

    @property
    def minimum_y(self):
        return (SettingsRacing.BETWEEN_LINE * SettingsRacing.MAX_VISIBLE_DISTANCE) + self.center_screen_y

    @property
    def maximum_y(self):
        return self.center_screen_y

    def perspective(self, distance: float):
        return self.depth * (distance + SettingsRacing.PERSPECTIVE_OFFSET)

    def project(
            self,
            distance: int,
            offset_x: int,
            curve_accumulator: int,
            elevator_accumulator: int
        ) -> RoadRacing:
        perspective = self.perspective(distance)
        inverse_perspective = 1.0 / perspective

        screen_x = self.center_screen_x + (curve_accumulator * inverse_perspective)
        screen_y = self.center_screen_y + (elevator_accumulator * inverse_perspective)

        road_width = (env.SCREEN_WIDTH * SettingsRacing.PERSPECTIVE_RATIO) * perspective

        y = int(SettingsRacing.BETWEEN_LINE * distance) + screen_y

        left_road = int(screen_x - road_width) + offset_x
        right_road = int(screen_x + road_width) + offset_x

        return RoadRacing(left_road, right_road, y)
    
    def stripe_wave(self,
            factor:float,
            duty: float,
            current_distance: float,
            visible_distance: float,
            road: RoadRacing
        ) -> bool:

        perspective = self.perspective(visible_distance + road.y)
        period = perspective * factor

        """
        virtual_phase = current_distance * SettingsRacing.WAVE_FACTOR
        current_phase = (visible_distance + road.y) / period
        continues_wave = (current_phase - virtual_phase) * 100.0

        return MathTools.rectangular_wave(continues_wave, 1.0, duty=0.5)
        """

        test = MathTools.rectangular_wave(period, 1.0, duty=duty)

        return test

    def event(self, event):
        '''
            Event management method
        '''
        pass

    def update(self, delta_time: float):
        """
            Update the renderer state.
        """
        previous_camera_distance = self.camera_distance

        self.camera_distance += (delta_time * self.speed)
        self.camera_distance %= self.racing_track.get_max_distance()

        # a reset occurred, reset the accumulators and the camera distance to remove any residue.
        if previous_camera_distance > self.camera_distance:
            self.laps += 1
            self.camera_distance = 0.0
            self.curve_accumulator = 0.0
            self.elevator_accumulator = 0.0

    def render(self, screen):
        """
            Render the racing method.
        """
        if self.racing_track is None:
            return
        
        screen.fill(ColorPalette.SKY)

        # center line (DEBUG)
        pygame.draw.line(screen, (255, 255, 255), (0, self.center_screen_y), (env.SCREEN_WIDTH, self.center_screen_y))

        # get the segment related to the camera.
        self.current_segment = self.racing_track.get_racing_sub_segment(distance=self.camera_distance)

        # curve and elevator integration along the camera segment
        # if we're still in the same segment, we're not going to increase it again.
        if self.current_segment != self.previous_segment:
            self.curve_accumulator += self.current_segment.racing_curve_factor
            self.elevator_accumulator += self.current_segment.racing_elevation_factor
            self.previous_segment = self.current_segment

        # render the road
        for visible_distance in range(0, SettingsRacing.MAX_VISIBLE_DISTANCE):
            current_distance = visible_distance + self.camera_distance

            road_a: RoadRacing = self.project(distance=visible_distance,
                                              offset_x=self.camera_offset,
                                              curve_accumulator=self.curve_accumulator,
                                              elevator_accumulator=self.elevator_accumulator
                                            )

            road_b: RoadRacing = self.project(distance=visible_distance + 1,
                                              offset_x=self.camera_offset,
                                              curve_accumulator=self.curve_accumulator,
                                              elevator_accumulator=self.elevator_accumulator
                                            )

            # interpolate the road between road_a and road_b to fill the gap between them.
            for (y) in range(int(road_a.y), int(road_b.y)):
                left_road = MathTools.lerp(road_a.left_road, road_b.left_road, (y - road_a.y) / (road_b.y - road_a.y))
                right_road = MathTools.lerp(road_a.right_road, road_b.right_road, (y - road_a.y) / (road_b.y - road_a.y))

                road = RoadRacing(left_road, right_road, y)

                self.render_road(screen,
                    visible_distance,
                    current_distance, 
                    road=road
                )

                self.render_stripe_center_road(
                    screen,
                    visible_distance,
                    current_distance,
                    road=road
                )

                self.render_stripe_border_road(
                    screen,
                    visible_distance,
                    current_distance,
                    road=road
                )

    def render_road(self,
                    screen,
                    visible_distance: float,
                    current_distance: float,
                    road: RoadRacing,
        ):
       pygame.draw.line(
           screen, 
           ColorPalette.ROAD, 
           (road.left_road, road.y), 
           (road.right_road, road.y)
        )
       
    def render_stripe_center_road(self,
                      screen,
                      visible_distance: float,
                      current_distance: float,
                      road: RoadRacing,
        ):
        road_factor = road.road_width * SettingsRacing.LANE_CENTER_RATIO

        if self.stripe_wave(
            SettingsRacing.LANE_CENTER_FACTOR,
            SettingsRacing.LANE_CENTER_DUTY,
            current_distance, 
            visible_distance, 
            road
        ):
            border_color = ColorPalette.WHITE
        else:
            border_color = ColorPalette.ROAD

        # Left Road
        pygame.draw.line(
           screen, 
           border_color, 
           (road._center_road - road_factor, road.y),
           (road._center_road + road_factor, road.y)
        )

    def render_stripe_border_road(self,
                      screen,
                      visible_distance: float,
                      current_distance: float,
                      road: RoadRacing,
        ):
        road_factor = road.road_width * SettingsRacing.LANE_BORDER_RATIO

        if self.stripe_wave(
            SettingsRacing.LANE_BORDER_FACTOR,
            SettingsRacing.LANE_BORDER_DUTY,
            current_distance, 
            visible_distance, 
            road
        ):
            border_color = ColorPalette.LANE_BORDER_A
        else:
            border_color = ColorPalette.LANE_BORDER_B

        # Left Road
        pygame.draw.line(
           screen, 
           border_color, 
           (road.left_road, road.y), 
           (road.left_road + road_factor, road.y)
        )

        # Right Road
        pygame.draw.line(
           screen, 
           border_color, 
           (road.right_road, road.y), 
           (road.right_road + road_factor, road.y)
        )
