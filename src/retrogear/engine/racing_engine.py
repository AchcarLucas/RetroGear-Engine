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
            elevator_accumulator: int,
            width_factor: float=1.0
        ) -> RoadRacing:
        perspective = self.perspective(slice_z)
        inverse_perspective = 1.0 / perspective

        screen_x = self.center_screen_x + (curve_accumulator * inverse_perspective)
        
        depth_y = SettingsRacing.BETWEEN_LINE * slice_z
        hill_y = elevator_accumulator * inverse_perspective
        relative_z = self.center_screen_y + depth_y - hill_y
    
        road_width = (env.SCREEN_WIDTH * SettingsRacing.PERSPECTIVE_RATIO) * width_factor * perspective

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

        # The 'self.speed' feature ensures that the animation follows the car's physics engine.
        position = road.absolute_z / 10.0

        # We maintain the logic of the inverse perspective that resolved the size issue.
        fator_perspectiva = 70.0 / (road.relative_z + 1.0)

        return MathTools.rectangular_wave(t=fator_perspectiva - position, p=factor * 0.75, duty=duty)

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

        #self.camera_z += (delta_time * self.speed)
        self.camera_z += self.speed
        self.camera_z %= self.racing_track.get_max_distance()

        # a reset occurred, reset the accumulators and the camera distance to remove any residue.
        if previous_camera_z > self.camera_z:
            self.laps += 1
            self.camera_z = 0.0

    def render(self, screen):
        """
            Render the racing method.
        """
        if self.racing_track is None:
            return
        
        screen.fill(ColorPalette.SKY)

        # center line (DEBUG)
        pygame.draw.line(screen, (255, 255, 255), (0, self.center_screen_y), (env.SCREEN_WIDTH, self.center_screen_y))
        
        heading_accumulator = 0.0
        curve_accumulator = 0.0
        elevator_accumulator = 0.0

        last_relative = env.SCREEN_HEIGHT

        for slice_z in reversed(range(0, SettingsRacing.MAX_VISIBLE_SLICE_Z)):
            world_z = slice_z + self.camera_z
           
            segment_a = self.racing_track.get_racing_sub_segment(distance=world_z)
            segment_b = self.racing_track.get_racing_sub_segment(distance=world_z + 1)

            road_a: RoadRacing = self.project(
                slice_z=slice_z,
                side_offset=self.camera_side_offset,
                curve_accumulator=curve_accumulator,
                elevator_accumulator=elevator_accumulator
            )

            heading_accumulator += (segment_a.racing_curve_factor + segment_b.racing_curve_factor) * 0.5
            curve_accumulator += heading_accumulator
            elevator_accumulator += (segment_a.racing_elevation_factor + segment_b.racing_elevation_factor) * 0.5

            road_b: RoadRacing = self.project(
                slice_z=slice_z + 1,
                side_offset=self.camera_side_offset,
                curve_accumulator=curve_accumulator,
                elevator_accumulator=elevator_accumulator
            )
            
            relative_a = int(road_a.relative_z)
            relative_b = int(road_b.relative_z)

            dy = relative_b - relative_a

            if relative_b >= last_relative or dy <= 0:
                continue

            last_relative = relative_b

            for (relative_z) in range(relative_a, relative_b + 1):
                t = (relative_z - relative_a) / dy
                left_road = MathTools.lerp(road_a.left_road, road_b.left_road, t)
                right_road = MathTools.lerp(road_a.right_road, road_b.right_road, t)

                road = RoadRacing(
                    left_road=left_road,
                    right_road=right_road,
                    relative_z=relative_z,
                    absolute_z=world_z,
                    relative_t=t
                )

                self.render_road(
                    screen,
                    road=road
                )

                self.render_stripe_border_line(
                    screen=screen,
                    road=road
                )

                self.render_stripe_center_line(
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
       
    def render_stripe_center_line(self,
                      screen,
                      road: RoadRacing
        ):
        line_factor = road.road_width * SettingsRacing.LANE_CENTER_RATIO

        if self.stripe_wave(
            road,
            SettingsRacing.LANE_CENTER_FACTOR,
            SettingsRacing.LANE_CENTER_DUTY
        ):
            border_color = ColorPalette.WHITE
        else:
            border_color = ColorPalette.ROAD

        road_offset = road.road_width * 0.385

        line_left = (road.left_road) + road_offset
        line_right = (road.right_road) - road_offset

         # Center Line
        pygame.draw.line(
           screen, 
           border_color, 
           (road._center_road - line_factor, road.relative_z),
           (road._center_road + line_factor, road.relative_z)
        )

        # Left Line
        pygame.draw.line(
           screen, 
           border_color, 
           (line_left - line_factor, road.relative_z),
           (line_left + line_factor, road.relative_z)
        )

        # Right Line
        pygame.draw.line(
           screen, 
           border_color, 
           (line_right - line_factor, road.relative_z),
           (line_right + line_factor, road.relative_z)
        )

    def render_stripe_border_line(self,
                      screen,
                      road: RoadRacing
        ):
        line_factor = road.road_width * SettingsRacing.LANE_BORDER_RATIO

        if self.stripe_wave(
            road,
            SettingsRacing.LANE_BORDER_FACTOR,
            SettingsRacing.LANE_BORDER_DUTY,
        ):
            border_color = ColorPalette.LANE_BORDER_A
        else:
            border_color = ColorPalette.LANE_BORDER_B

        # Left Line
        pygame.draw.line(
           screen, 
           border_color, 
           (road.left_road, road.relative_z), 
           (road.left_road + line_factor, road.relative_z)
        )
    
        # Right Line
        pygame.draw.line(
           screen, 
           border_color, 
           (road.right_road, road.relative_z), 
           (road.right_road + line_factor, road.relative_z)
        )

