from src.utils.singleton_meta import SingletonMeta

class LocatorManager(metaclass=SingletonMeta):
    _locators = []

    def add_locator(self, locator_name, locator_instance):
        self._locators.append({locator_name : locator_instance})

    def get_locator(self, locator_name):
        for locator in self._locators:
            if locator_name in locator:
                return locator[locator_name]
        return None
