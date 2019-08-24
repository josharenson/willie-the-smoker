from typing import Callable

import atexit
import threading


class Observable(object):

    def __init__(self):
        self._observers = {}
        self._main_event = threading.Event()
        self._running = False
        self._worker = None  # Create on demand as threads can't be reused

        atexit.register(self._stop)

    def add_observer(self, event_name: str, observer: Callable):
        print("Adding observer for {}".format(event_name))
        if event_name not in self._observers:
            self._observers[event_name] = []
        self._observers[event_name].append(observer)
        if not self._running:
            self._worker = threading.Thread(target=self.event_loop)
            self._running = True
            self._worker.start()

    # Default event loop does nothing but can be overridden
    # This design means clients, like smoked, don't need to do
    # any thread managment and can just chug along until there is nothing
    # left to observe
    def event_loop(self):
        self._main_event.wait()

    def property_changed(self, property_name: str, value):
        if property_name not in self._observers:
            return
        for observer in self._observers[property_name]:
            observer(value)

    def remove_observer(self, event_name: str,  observer: Callable):
        print("Removing observer for {}".format(event_name))
        if event_name not in self._observers:
            return
        for i in range(len(self._observers[event_name])):
            if self._observers[event_name][i] == observer:
                del(self. _observers[event_name][i])
                if not self._observers[event_name]:
                    del(self._observers[event_name])
        if not len(self._observers):
            self._stop()

    def _stop(self):
        self._running = False
        self._main_event.set()
        if self._worker is not None:
            self._worker.join()
