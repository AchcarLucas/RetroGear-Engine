import pygame
import sys

from src.retrogear.interface.engine_interface import IEngine

from src.retrogear.engine.racing_engine import RacingEngine

from src.retrogear.racing.track_racing import TrackRacing
from src.retrogear.racing.segment_racing import SegmentRacing

from src.retrogear.utils.color_palette import ColorPalette

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RetroGearEngine(IEngine):
    def __init__(self,
                 caption="Retro Gear - Engine",
                 screen_width=800,
                 screen_height=600,
                 fps=60
        ):
        self.caption = caption

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.fps = fps

        self.init()
        self.test()

    def init(self):
        '''
            Pygame initialization
        '''
        pygame.init()

        logging.info(f"screen_width: {self.screen_width}")
        logging.info(f"screen_height: {self.screen_height}")

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE

        # configurações da tela
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            flags
        )

        pygame.display.set_caption(self.caption)

        # configuração do relógio e do fps
        self.clock = pygame.time.Clock()

        # configuração da fonte
        self.font = pygame.font.SysFont(None, 24)

    def test(self):
        '''
            Engine testing method
        '''
        self.racing_render = RacingEngine()
        self.racing_track = TrackRacing()

        # reta
        self.racing_track.append(SegmentRacing(1000, 1.0, 0.0, 0.0))
        # curva direita
        self.racing_track.append(SegmentRacing(70, 1.0, 0.01, 0.0))
        # curva direita (reverted)
        self.racing_track.append(SegmentRacing(70, 1.0, -0.01, 0.0))
        # hill
        self.racing_track.append(SegmentRacing(70, 1.0, 0.0, 0.1))
        # hill (reverted)
        self.racing_track.append(SegmentRacing(70, 1.0, 0.0, -0.1))
        # curva esquerda
        self.racing_track.append(SegmentRacing(90, 1.0, -0.015, -0.3))
        # curva esquerda (reverted)
        self.racing_track.append(SegmentRacing(90, 1.0, 0.015, 0.3))
        # reta
        self.racing_track.append(SegmentRacing(200, 1.0, 0.0, 0.0))

        logging.info(f"Racing track: {self.racing_track}")

        self.racing_render.set_racing_track(self.racing_track)

    def run(self):
        '''
            Main Loop
        '''
        self.running = True

        while self.running:
            delta_time = self.clock.tick(self.fps) / 1000.0  # Convert to seconds
            self.screen.fill((0, 0, 0))

            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.screen.blit(fps_text, (10, 10))

            for event in pygame.event.get():
                self.event(event)

            self.update(delta_time)
            self.render()

            pygame.display.flip()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def event(self, event):
        '''
            Event management method
        '''
        if(event.type == pygame.QUIT):
            self.running = False
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                self.running = False

        self.racing_render.event(event)

    def update(self, delta_time):
        '''
            Logic management method
        '''
        self.racing_render.update(delta_time)

    def render(self):
        '''
            Rendering management method
        '''
        self.screen.fill(ColorPalette.BG_COLOR)

        self.racing_render.render(self.screen)

        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        pygame.display.flip()