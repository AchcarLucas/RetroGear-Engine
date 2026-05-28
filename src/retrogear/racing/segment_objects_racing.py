from __future__ import annotations

from src.manager.locator_manager import LocatorManager

locator = LocatorManager()

# getting configuration manager
env = locator.get_locator('env')

# getting logging manager
logging = locator.get_locator('logging')

class SegmentObjectsRacing():
    def __init__(self, objects: list = []):
        self.objects = objects

    @classmethod
    def join(cls,
             parent_a: SegmentObjectsRacing,
             parent_b: SegmentObjectsRacing
        ):
        return cls(
            parent_a.objects + parent_b.objects
        )
