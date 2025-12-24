from abc import ABC, abstractmethod

class IEngine(ABC):
    @abstractmethod
    def event(self, event):
        raise NotImplementedError("Method event not implemented")

    @abstractmethod
    def update(self, delta_time):
        raise NotImplementedError("Method update not implemented")

    @abstractmethod
    def render(self, screen):
        raise NotImplementedError("Method screen not implemented")