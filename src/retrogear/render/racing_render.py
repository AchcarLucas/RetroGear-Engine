import pygame

from src.retrogear.interface.engine_interface import IEngine

from src.retrogear.racing.track_racing import TrackRacing
from src.retrogear.racing.segment_racing import SubSegmentRacing, SegmentColorsRacing, SegmentObjectsRacing
from src.retrogear.racing.settings_racing import SettingsRacing
from src.retrogear.racing.road_racing import RoadRacing, ColorsRacing, ObjectsRacing

from src.retrogear.utils.color_palette import ColorPalette
from src.retrogear.utils.math_tools import MathTools

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RacingRender(IEngine):
    def __init__(self, racing_track: TrackRacing=None):
        self.racing_track = racing_track

        self.center_screen_x: int = env.SCREEN_WIDTH // 2
        self.center_screen_y: int = env.SCREEN_HEIGHT // 2

        self.depth: float = SettingsRacing.MAX_VISIBLE_SLICE_Z * SettingsRacing.DEPTH_FACTOR

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

    def perspective(self, distance: float):
        return self.depth / (distance + 0.1)

    def project(
            self,
            slice_z: int,
            side_offset: int,
            curve_accumulator: int,
            elevator_accumulator: int,
            width_factor: float=1.0
        ) -> RoadRacing:
        perspective = self.perspective(slice_z)

        relative_z = self.center_screen_y - elevator_accumulator + (SettingsRacing.CAMERA_HEIGHT * perspective)
        relative_x = self.center_screen_x + (curve_accumulator * perspective)

        road_width = env.SCREEN_WIDTH * (width_factor * perspective) * SettingsRacing.ROAD_WIDTH_PERSPECTIVE
        left_road = int(relative_x - road_width) + side_offset
        right_road = int(relative_x + road_width) + side_offset

        return RoadRacing(
            slice_z=slice_z,
            left_road=left_road,
            right_road=right_road,
            relative_z=relative_z,
            width_factor=width_factor
        )
    
    def project_road(self):
        p_road: [RoadRacing] = []

        heading_accumulator = 0.0
        curve_accumulator = 0.0
        elevator_accumulator = 0.0

        # project road
        for slice_z in range(0, SettingsRacing.MAX_VISIBLE_SLICE_Z):
            world_z = self.camera_z + slice_z

            segment = self.racing_track.get_racing_sub_segment(distance=world_z)

            heading_accumulator += segment.racing_curve_factor
            curve_accumulator += heading_accumulator
            elevator_accumulator += segment.racing_elevation_factor

            road: RoadRacing = self.project(
                slice_z=slice_z,
                side_offset=0,
                curve_accumulator=curve_accumulator,
                elevator_accumulator=elevator_accumulator,
                width_factor=segment.racing_width_factor
            )

            p_road.append((road, segment))

        return p_road

    def lerp_road(self, p_road):
        r_road: [RoadRacing] = []

        # lerp road line to next road line 
        for index_road in range(0, len(p_road)):
            current_road: RoadRacing = p_road[index_road - 1][0]
            road_next: RoadRacing = p_road[index_road][0]

            segment: SubSegmentRacing = p_road[index_road - 1][1]

            dy = current_road.relative_z - road_next.relative_z

            # If the segment is behind something already drawn (hill clipping), we ignore it.
            if dy <= 0.00:
                continue

            relative_current = int(MathTools.ceil(current_road.relative_z))
            relative_next = int(MathTools.ceil(road_next.relative_z))

            # lerp road with current road and next road
            for relative_z in range(relative_next, relative_current):
                t = (relative_z - relative_next) / dy

                left_road = MathTools.lerp(road_next.left_road, current_road.left_road, t)
                right_road = MathTools.lerp(road_next.right_road, current_road.right_road, t)
                width_road = MathTools.lerp(road_next.width_factor, current_road.width_factor, t)

                t_road:RoadRacing = RoadRacing(
                    left_road=left_road,
                    right_road=right_road,
                    slice_z=current_road.slice_z,
                    relative_z=relative_z,
                    absolute_z=current_road.absolute_z,
                    relative_t=t,
                    width_factor=width_road
                )
                
                r_road.append((t_road, segment))

        return r_road
    
    def stribe_mod(self,
            road: RoadRacing,
            factor:float = 1.0,
        ) -> bool:
    
        stribe = road.slice_z
        displacement = self.camera_z

        phase = (stribe + displacement + 1.0) / factor

        return MathTools.floor(phase) % 2

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

    def render(self, screen):
        """
            Render the racing method.
        """
        if self.racing_track is None:
            return

        p_road = self.project_road()
        r_road = self.lerp_road(p_road)

        # draw sky        
        screen.fill(ColorPalette.SKY)

        # draw road line
        for road, segment in reversed(r_road):
            self.render_road(
                screen,
                road=road,
                colors=segment.racing_colors,
                objects=segment.racing_objects
            )

            self.render_stribe_track_line(
                screen=screen,
                road=road,
                colors=segment.racing_colors,
                objects=segment.racing_objects
            )

            self.render_stribe_border_line(
                screen=screen,
                road=road,
                colors=segment.racing_colors,
                objects=segment.racing_objects
            )

    def render_road(self,
                    screen,
                    road: RoadRacing,
                    colors: ColorsRacing,
                    objects: ObjectsRacing
        ):
        if self.stribe_mod(
            road,
            SettingsRacing.LANE_TRACK_STRIBE_FACTOR
        ):
            road_color = colors.road_color_a
            slope_color = colors.glass_color_a
        else:
            road_color = colors.road_color_b
            slope_color = colors.glass_color_b

        # draw road
        pygame.draw.line(
            screen, 
            road_color,
            (road.left_road, road.relative_z),
            (road.right_road, road.relative_z)
        )

        # draw slope (left and right)
        pygame.draw.line(
            screen, 
            slope_color,
            (0, road.relative_z),
            (road.left_road, road.relative_z)
        )

        pygame.draw.line(
            screen, 
            slope_color,
            (road.right_road, road.relative_z),
            (env.SCREEN_WIDTH, road.relative_z)
        )
       
    def render_stribe_track_line(self,
                      screen,
                      road: RoadRacing,
                      colors: ColorsRacing,
                      objects: ObjectsRacing
        ):
    
        if self.stribe_mod(
            road,
            SettingsRacing.LANE_TRACK_STRIBE_FACTOR
        ):
            stribe_color = ColorPalette.WHITE
        else:
            stribe_color = colors.road_color_b

        n_lanes = max(1, int(road.width_factor))

        road_width_normalized = MathTools.normalize(road.road_width / road.width_factor, 0.0, 1.0) * 0.5
        lane_width_factor = road_width_normalized * SettingsRacing.LANE_TRACK_WIDTH_FACTOR

        line_left = line_right = road.center_road

        offset = road_width_normalized * 0.5

        for i in range(0, n_lanes):
            if i == 0:
                line_left += offset / 2
                line_right -= offset / 2
            else:
                line_left += offset * 1.5
                line_right -= offset * 1.5

            # Left Line
            pygame.draw.line(
                screen, 
                stribe_color, 
                (line_left - lane_width_factor, road.relative_z),
                (line_left + lane_width_factor, road.relative_z)
            )

            # Right Line
            pygame.draw.line(
                screen, 
                stribe_color, 
                (line_right - lane_width_factor, road.relative_z),
                (line_right + lane_width_factor, road.relative_z)
            )

    def render_stribe_border_line(self,
                      screen,
                      road: RoadRacing,
                      colors: ColorsRacing,
                      objects: ObjectsRacing
        ):
        if self.stribe_mod(
            road,
            SettingsRacing.LANE_BORDER_STRIBE_FACTOR
        ):
            stribe_color = colors.lane_border_color_a
        else:
            stribe_color = colors.lane_border_color_b

        road_width_normalized = MathTools.normalize(road.road_width / road.width_factor, 0.0, 1.0)
        lane_width_factor = road_width_normalized * SettingsRacing.LANE_BORDER_WIDTH_FACTOR

        # Left Line
        pygame.draw.line(
           screen, 
           stribe_color,
           (road.left_road - lane_width_factor, road.relative_z), 
           (road.left_road + lane_width_factor, road.relative_z)
        )
    
        # Right Line
        pygame.draw.line(
           screen, 
           stribe_color,
           (road.right_road - lane_width_factor, road.relative_z), 
           (road.right_road + lane_width_factor, road.relative_z)
        )

