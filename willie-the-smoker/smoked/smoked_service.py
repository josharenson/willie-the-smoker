# External deps
import json
import logging
import pika
import sys

# Internal deps
from common import events
from common.singleton import Singleton
from hal.relay import Relay
from hal.thermometers import Thermometers

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

        # Initialize Relay
        self.relay = Relay()
        self.relay.add_observer(events.RELAY_ACTIVE, self._on_relay_active_changed)

        # Initialize Thermometers
        self.thermometers = Thermometers(sensor_poll_interval_s, simulate=simulate)
        self.thermometers.add_observer(events.TEMP_CHANGED, self._on_temperature_changed)

    @staticmethod
    def _on_relay_active_changed(value: bool):
        msg = {events.RELAY_ACTIVE: value}
        this = SmokeDService()
        this.channel.basic_publish(exchange='',
                                   routing_key=events.SMOKED_QUEUE_NAME,
                                   body=json.dumps(msg))

    @staticmethod
    def _on_temperature_changed(temperatures: dict):
        msg = {events.TEMP_CHANGED: temperatures}
        this = SmokeDService()
        this.channel.basic_publish(exchange='',
                                   routing_key=events.SMOKED_QUEUE_NAME,
                                   body=json.dumps(msg))

    def stop(self):
        self.relay.remove_observer(events.RELAY_ACTIVE, self._on_relay_active_changed)
        self.thermometers.remove_observer(events.TEMP_CHANGED, self._on_temperature_changed)
        self.channel.queue_delete(events.SMOKED_QUEUE_NAME)
        self.connection.close()
