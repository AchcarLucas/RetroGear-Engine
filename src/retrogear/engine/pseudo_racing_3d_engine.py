import pygame

from src.manager.locator_manager import LocatorManager

from src.retrogear.interface.engine_interface import IEngine

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

"""
    Racing Engine é apenas uma 'prova de conceito' do Pseudo-3D Racing
"""
class RacingEngine(IEngine):
    def __init__(self):
        pass

    def event(self, event):
        '''
            gerenciamento de event da engine
        '''
        pass

    def update(self, delta_time):
        '''
            gerenciamento da lógica da engine
        '''
        pass

    def render(self):
        '''
            gerenciamento da renderização da engine
        '''
        pass