# External deps
from unittest.mock import MagicMock
from waiting import wait

import json
import pika
import unittest

# Internal eps
from common.event_listener import EventListener


class TestEventListener(unittest.TestCase):

    def setUp(self):
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))

    def tearDown(self):
        self.connection.close()

    def test_callbacks(self):
        queue_name = "IGottaGetDrunk"
        event_listener = EventListener(queue_name)

        heartbreak_hotel_event_name = "heartbreak_hotel"
        heartbreak_hotel_callback = MagicMock()
        event_listener.add_listener(heartbreak_hotel_event_name, heartbreak_hotel_callback)

        channel = self.connection.channel()
        channel.queue_declare(queue_name)

        event_listener.start()
        data = json.dumps({heartbreak_hotel_event_name: "some data"})
        channel.basic_publish("", queue_name, data)

        wait(lambda: heartbreak_hotel_callback.called, timeout_seconds=5)
        self.assertTrue(heartbreak_hotel_callback.called)

        event_listener.stop()
