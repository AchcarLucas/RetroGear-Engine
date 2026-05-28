from src.retrogear.interface.engine_interface import IEngine

class RacingRender(IEngine):
     def event(self, event):
        '''
            Event management method
        '''
        pass

    def update(self, delta_time: float):
        """
            Update the renderer state.
        """
        pass

    def render(self, screen):
        """
            Render the racing method.
        """
        pass