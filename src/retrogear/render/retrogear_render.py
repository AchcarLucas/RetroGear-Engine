import pygame
import sys

from src.retrogear.interface.render_interface import IRender

from src.retrogear.render.racing_render import RacingRenderer

from src.retrogear.engine.racing_track import RacingTrack
from src.retrogear.engine.racing_segment import RacingSegment

from src.retrogear.utils.color_palette import ColorPalette

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class RetroGearRender(IRender):
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
        # inicialização do pygame
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
            método de teste da engine
        '''
        self.racing_render = RacingRenderer()

        racing_segment_list = []

        # inicio do segmento
        racing_segment_list.append(RacingSegment(1, 1.0, 0.0, 0.0))
        # segmentos intermediários
        racing_segment_list.append(RacingSegment(20, 1.0, 0.0, 0.0))
        # racing_segment_list.append(RacingSegment(30, 1.0, 50.0, 0.0))
        racing_segment_list.append(RacingSegment(30, 1.0, 10.0, 0.0))
        racing_segment_list.append(RacingSegment(30, 1.0, 10.0, 0.0))
        racing_segment_list.append(RacingSegment(30, 1.0, -10.0, 0.0))
        racing_segment_list.append(RacingSegment(30, 1.0, -10.0, 0.0))
        racing_segment_list.append(RacingSegment(30, 1.0, 0.0, 10.0))
        racing_segment_list.append(RacingSegment(30, 1.0, 0.0, 10.0))
        racing_segment_list.append(RacingSegment(30, 1.0, 0.0, -10.0))
        racing_segment_list.append(RacingSegment(30, 1.0, 0.0, -10.0))
        # racing_segment_list.append(RacingSegment(30, 1.0, -50.0, 0.0))
        # racing_segment_list.append(RacingSegment(30, 1.0, -50.0, 0.0))
        # racing_segment_list.append(RacingSegment(50, 1.0, 0.0, 0.0))
        racing_segment_list.append(RacingSegment(50, 1.0, 0.0, 0.0))
        # final do segmento
        racing_segment_list.append(RacingSegment(1, 1.0, 0.0, 0.0))

        self.racing_track = RacingTrack(
            racing_segment_list
        )

        self.racing_track.generate_racing_track()

        self.racing_render.set_racing_track(self.racing_track)

        logging.info(self.racing_track)
        logging.info(self.racing_track.get_racing_sub_segment(0))
        logging.info(self.racing_track.get_racing_sub_segment(1))
        logging.info(self.racing_track.get_racing_sub_segment(2))
        logging.info(self.racing_track.get_racing_sub_segment(3))
        logging.info(self.racing_track.get_racing_sub_segment(1200))
        logging.info(self.racing_track.get_racing_sub_segment(1201))
        logging.info(self.racing_track.get_racing_sub_segment(1202))
        logging.info(self.racing_track.get_racing_sub_segment(1203))
        logging.info(self.racing_track.get_racing_sub_segment(1204))
        logging.info(self.racing_track.get_racing_sub_segment(1205))
        logging.info(self.racing_track.get_racing_sub_segment(1206))
        logging.info(self.racing_track.get_racing_sub_segment(1207))
        logging.info(self.racing_track.get_racing_sub_segment(1208))

    def run(self):
        '''
            loop principal da engine
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
            gerenciamento de event da engine
        '''
        if(event.type == pygame.QUIT):
            self.running = False
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                self.running = False

    def update(self, delta_time):
        '''
            gerenciamento da lógica da engine
        '''
        self.racing_render.update(delta_time)

    def render(self):
        '''
            gerenciamento da renderização da engine
        '''
        self.screen.fill(ColorPalette.BG_COLOR)

        self.racing_render.render(self.screen)

        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        pygame.display.flip()