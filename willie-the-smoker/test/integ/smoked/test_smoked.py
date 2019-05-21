# External deps
from unittest.mock import MagicMock

import json
import pika
import time
import unittest

# Internal deps
from common import events
from smoked.smoked_service import SmokeDService


class TestSmoked(unittest.TestCase):

    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    def tearDown(self):
        self.connection.close()

    @classmethod
    def tearDownClass(cls):
        smoked = SmokeDService()
        smoked.stop()

    def test_relay_changed(self):
        smoked = SmokeDService()

        channel = self.connection.channel()
        channel.queue_declare(queue=events.SMOKED_QUEUE_NAME)

        self.assertFalse(smoked.relay.active)
        smoked.relay.active = True

        method, header, body = channel.basic_get(events.SMOKED_QUEUE_NAME, auto_ack=True)

        res_obj = json.loads(body.decode('utf-8'))
        actual_result = res_obj[events.RELAY_ACTIVE]
        expected_result = True
        self.assertEqual(actual_result, expected_result)

    def test_temp_changed(self):
        poll_interval_s = 0.5
        smoked = SmokeDService(sensor_poll_interval=poll_interval_s)
        initial_temp_reading = smoked.thermometers.get_temperature("")
        smoked.thermometers._read_temp = MagicMock()
        smoked.thermometers._read_temp.return_value = initial_temp_reading

        channel = self.connection.channel()
        channel.queue_declare(queue=events.SMOKED_QUEUE_NAME)

        self.assertEqual(smoked.thermometers.get_temperature(""), initial_temp_reading)

        updated_temp_val = 420.69
        smoked.thermometers._read_temp.return_value = updated_temp_val
        time.sleep(2 * poll_interval_s)

        method, header, body = channel.basic_get(events.SMOKED_QUEUE_NAME, auto_ack=True)

        res_obj = json.loads(body.decode('utf-8'))
        actual_result = res_obj[events.TEMP_CHANGED]
        expected_result = updated_temp_val
        self.assertEqual(actual_result, expected_result)
