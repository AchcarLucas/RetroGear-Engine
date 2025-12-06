import pygame
import sys

class RetroGearEngine():
    def __init__(self, caption="Retro Gear Engine", screen_width=800, screen_height=600, fps=60):
        self.caption = caption
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps

        self.init()

    def init(self):
        # inicialização do pygame
        pygame.init()

        # configurações da tela
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.caption)

        # configuração do relógio e do fps
        self.clock = pygame.time.Clock()

    def run(self):
        '''
            Loop principal da engine
        '''
        self.running = True

        while self.running:
            delta_time = self.clock.tick(self.fps)
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                self.event(event)

            self.update(delta_time)
            self.render()

            pygame.display.flip()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def event(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self):
        pass