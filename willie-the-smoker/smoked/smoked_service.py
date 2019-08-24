import pdb
# External deps
import json
import logging
import pika
import sys

# Internal deps
from common import events
from common.singleton import Singleton
from smoked.thermostat import Thermostat

LOG = logging.getLogger(__name__)


class SmokeDService(object, metaclass=Singleton):

    def __init__(self, sensor_poll_interval_s=10, simulate=False):
        # Initialize logger
        LOG.setLevel(logging.DEBUG)
        fh = logging.FileHandler("smoked.log")
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        LOG.addHandler(fh)
        LOG.addHandler(ch)
        LOG.debug("Logging initialized...")

        # Initialize message queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(events.SMOKED_QUEUE_NAME)

        # Initialize thermostat
        self.thermostat = Thermostat(sensor_poll_interval_s, simulate)

    def _on_relay_active_changed(self, value: bool):
        LOG.debug("Relay active changed-> {}".format(value))
        msg = {events.RELAY_ACTIVE: value}
        self.channel.basic_publish(exchange='',
                                   routing_key=events.SMOKED_QUEUE_NAME,
                                   body=json.dumps(msg))

    def _on_temperature_changed(self, temperatures: dict):
        msg = {events.TEMP_CHANGED: temperatures}
        self.channel.basic_publish(exchange='',
                                   routing_key=events.SMOKED_QUEUE_NAME,
                                   body=json.dumps(msg))

    def start(self):
        self.thermostat.add_observer(events.RELAY_ACTIVE, self._on_relay_active_changed)
        self.thermostat.add_observer(events.TEMP_CHANGED, self._on_temperature_changed)
        self.thermostat.start()

    def stop(self):
        self.thermostat.stop()
        self.thermostat.remove_observer(events.RELAY_ACTIVE, self._on_relay_active_changed)
        self.thermostat.remove_observer(events.TEMP_CHANGED, self._on_temperature_changed)
        if self.channel.is_open:
            self.channel.queue_delete(events.SMOKED_QUEUE_NAME)
        if self.connection.is_open:
            self.connection.close()
