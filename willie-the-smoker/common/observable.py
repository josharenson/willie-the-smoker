from typing import Callable

class Observable(object):

    def __init__(self):
        self._observers = {}

    def add_observer(self, event_name: str, observer: Callable):
        if (event_name not in self._observers):
            self._observers[event_name] = []
        self._observers[event_name].append(observer)

    def property_changed(self, property_name: str, value):
        for observer in self._observers[property_name]:
            observer(value)

