from typing import Callable

class Observable(object):

    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Callable):
        self._observers.append(observer)

    def property_changed(self, property_name: str, value):
        for observer in self._observers:
            observer(property_name, value)

