import pdb
from typing import Callable

class Observable(object):

    def __init__(self):
        self._observers = {}

    def add_observer(self, event_name: str, observer: Callable):
        if event_name not in self._observers:
            self._observers[event_name] = []
        self._observers[event_name].append(observer)

    def property_changed(self, property_name: str, value):
        if property_name not in self._observers:
            return
        for observer in self._observers[property_name]:
            observer(value)

    def remove_observer(self, event_name: str,  observer: Callable):
        if event_name not in self._observers:
            return
        for _observer in self._observers[event_name]:
            if _observer is observer:
               self. _observers[event_name].remove(observer)
               if not self._observers[event_name]:
                   del(self._observers[event_name])

