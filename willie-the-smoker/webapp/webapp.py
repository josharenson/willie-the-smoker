# External deps
from flask import Flask, Response, render_template
from flask_scss import Scss

import hashlib
import json
import logging
import threading
import time

# Internal deps
from common.events import (
        RELAY_ACTIVE,
        TEMP_CHANGED,
        SMOKED_QUEUE_NAME
)
from common.event_listener import EventListener

LOG = logging.getLogger(__name__)


class SensorMonitor(object):

    def __init__(self, queue_name):
        self.event_listener = EventListener(queue_name)

        self._relay_active = False
        self._relay_active_lock = threading.Lock()
        self.event_listener.add_listener(RELAY_ACTIVE, self.set_relay_active)

        self._current_temps = {}
        self._current_temps_lock = threading.Lock()
        self.event_listener.add_listener(TEMP_CHANGED, self._on_temps_changed)

    @property
    def current_temps(self):
        return self._current_temps

    def _on_temps_changed(self, value):
        self._current_temps = value

    @property
    def relay_active(self):
        return self._relay_active

    def set_relay_active(self, value: bool):
        with self._relay_active_lock:
            self._relay_active = value

    def start(self):
        self.event_listener.start()

    def stop(self):
        self.event_listener.stop()


def create_app(*args, **kwargs):
    app = Flask(__name__)
    app.debug = True
    Scss(app)

    @app.route("/stream")
    def stream():
        s = SensorMonitor(SMOKED_QUEUE_NAME)
        s.start()

        def _stream():
            last_sha = 0
            while True:
                time.sleep(1)
                response = {}
                print("Relay active-> {}".format(s.relay_active))
                response["current_temps"] = s.current_temps
                response["relay_active"] = s.relay_active
                the_json = json.dumps(response)
                this_sha = hashlib.sha256()
                this_sha.update(the_json.encode())
                this_sha = this_sha.hexdigest()
                if this_sha != last_sha:
                    yield "data: {}\n\n".format(json.dumps(response))
                last_sha = this_sha

        return Response(_stream(),
                        mimetype="text/event-stream")

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    return app


app = create_app()
