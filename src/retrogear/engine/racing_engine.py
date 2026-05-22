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

        self.depth: float = (self.center_screen_y / SettingsRacing.MAX_VISIBLE_SLICE_Z) * SettingsRacing.DEPTH_FACTOR

        self.current_segment: SubSegmentRacing = None
        self.previous_segment: SubSegmentRacing = None

        self.laps: int = 0
        self.camera_z: float = 0.0
        self.camera_side_offset: float = 0.0

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
            slice_z: int,
            side_offset: int,
            curve_accumulator: int,
            elevator_accumulator: int
        ) -> RoadRacing:
        perspective = self.perspective(slice_z)
        inverse_perspective = 1.0 / perspective

        screen_x = self.center_screen_x + (curve_accumulator * inverse_perspective)
        screen_y = self.center_screen_y + (elevator_accumulator * inverse_perspective)

        road_width = (env.SCREEN_WIDTH * SettingsRacing.PERSPECTIVE_RATIO) * perspective

        relative_z = int(SettingsRacing.BETWEEN_LINE * slice_z) + screen_y

        left_road = int(screen_x - road_width) + side_offset
        right_road = int(screen_x + road_width) + side_offset

        return RoadRacing(
            left_road=left_road,
            right_road=right_road,
            relative_z=relative_z
        )
    
    def stripe_wave(self,
            road: RoadRacing,
            factor:float,
            duty: float,
        ) -> bool:

        perspective = self.perspective(road.absolute_z)
        period = perspective * 0.25 * 50.0

        virtual_phase = road.absolute_z / period
        current_phase = (road.relative_z + road.relative_z) / period
        continues_wave = (current_phase - virtual_phase)

        return MathTools.rectangular_wave(continues_wave, 1.0, duty=duty)

    def event(self, event):
        '''
            Event management method
        '''
        pass

    def update(self, delta_time: float):
        """
            Update the renderer state.
        """
        previous_camera_z = self.camera_z

        self.camera_z += (delta_time * self.speed)
        self.camera_z %= self.racing_track.get_max_distance()

        # a reset occurred, reset the accumulators and the camera distance to remove any residue.
        if previous_camera_z > self.camera_z:
            self.laps += 1
            self.camera_z = 0.0
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
        self.current_segment = self.racing_track.get_racing_sub_segment(distance=self.camera_z)

        # curve and elevator integration along the camera segment
        # if we're still in the same segment, we're not going to increase it again.
        if self.current_segment != self.previous_segment:
            self.curve_accumulator += self.current_segment.racing_curve_factor
            self.elevator_accumulator += self.current_segment.racing_elevation_factor
            self.previous_segment = self.current_segment

        # render the road
        for slice_z in range(0, SettingsRacing.MAX_VISIBLE_SLICE_Z):
            road_a: RoadRacing = self.project(slice_z=slice_z,
                                              side_offset=self.camera_side_offset,
                                              curve_accumulator=self.curve_accumulator,
                                              elevator_accumulator=self.elevator_accumulator
                                            )

            road_b: RoadRacing = self.project(slice_z=slice_z + 1,
                                              side_offset=self.camera_side_offset,
                                              curve_accumulator=self.curve_accumulator,
                                              elevator_accumulator=self.elevator_accumulator
                                            )

            # interpolate the road between road_a and road_b to fill the gap between them.
            for (relative_z) in range(int(road_a.relative_z), int(road_b.relative_z)):
                t = (relative_z - road_a.relative_z) / (road_b.relative_z - road_a.relative_z)
                left_road = MathTools.lerp(road_a.left_road, road_b.left_road, t)
                right_road = MathTools.lerp(road_a.right_road, road_b.right_road, t)

                absolute_z = relative_z + self.camera_z

                road = RoadRacing(
                    left_road=left_road,
                    right_road=right_road,
                    relative_z=relative_z,
                    absolute_z=absolute_z
                )

                self.render_road(
                    screen,
                    road=road
                )

                self.render_stripe_center_road(
                    screen=screen,
                    road=road
                )

                self.render_stripe_border_road(
                    screen=screen,
                    road=road
                )

    def render_road(self,
                    screen,
                    road: RoadRacing,
        ):
       pygame.draw.line(
           screen, 
           ColorPalette.ROAD, 
           (road.left_road, road.relative_z), 
           (road.right_road, road.relative_z)
        )
       
    def render_stripe_center_road(self,
                      screen,
                      road: RoadRacing
        ):
        road_factor = road.road_width * SettingsRacing.LANE_CENTER_RATIO

        if self.stripe_wave(
            road,
            SettingsRacing.LANE_CENTER_FACTOR,
            SettingsRacing.LANE_CENTER_DUTY
        ):
            border_color = ColorPalette.WHITE
        else:
            border_color = ColorPalette.ROAD

        # Center Road
        pygame.draw.line(
           screen, 
           border_color, 
           (road._center_road - road_factor, road.relative_z),
           (road._center_road + road_factor, road.relative_z)
        )

    def render_stripe_border_road(self,
                      screen,
                      road: RoadRacing
        ):
        road_factor = road.road_width * SettingsRacing.LANE_BORDER_RATIO

        if self.stripe_wave(
            road,
            SettingsRacing.LANE_BORDER_FACTOR,
            SettingsRacing.LANE_BORDER_DUTY,
        ):
            border_color = ColorPalette.LANE_BORDER_A
        else:
            border_color = ColorPalette.LANE_BORDER_B

        # Left Road
        pygame.draw.line(
           screen, 
           border_color, 
           (road.left_road, road.relative_z), 
           (road.left_road + road_factor, road.relative_z)
        )

        # Right Road
        pygame.draw.line(
           screen, 
           border_color, 
           (road.right_road, road.relative_z), 
           (road.right_road + road_factor, road.relative_z)
        )
