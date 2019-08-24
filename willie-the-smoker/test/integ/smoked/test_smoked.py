# External deps

import pika
import time
import unittest

# Internal deps
from unittest.mock import MagicMock
from smoked.smoked_service import SmokeDService

POLL_INTERVAL = 1


class TestSmoked(unittest.TestCase):

    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.instance = SmokeDService(POLL_INTERVAL, True)

    def tearDown(self):
        self.connection.close()
        self.instance.stop()
        SmokeDService.delete_instance()

    def test_initial_state(self):
        expected_initial_relay_state = False  # Safety first bro
        initial_relay_state = self.instance.thermostat.relay.active
        self.assertEqual(expected_initial_relay_state, initial_relay_state)

    def test_thermostat(self):
        self.instance._on_temperature_changed = MagicMock()
        self.instance.start()
        time.sleep(POLL_INTERVAL)
        self.assertTrue(self.instance._on_temperature_changed.called)
