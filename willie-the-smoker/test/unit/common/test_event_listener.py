# External deps
from unittest.mock import MagicMock
import unittest

# Internal deps
from common.event_listener import EventListener


class TestEventListener(unittest.TestCase):

    def test_adding_listeners(self):
        event_listener = EventListener("WhiskeyRiver")

        luckenbach_event_name = "luckenbach"
        luckenbach_callback = MagicMock()
        event_listener.add_listener(luckenbach_event_name, luckenbach_callback)

        self.assertTrue(luckenbach_event_name in event_listener._events)
        actual_len = len(event_listener._events[luckenbach_event_name])
        expected_len = 1
        self.assertEqual(actual_len, expected_len)

        # Can add the same callback twice
        event_listener.add_listener(luckenbach_event_name, luckenbach_callback)
        actual_len = len(event_listener._events[luckenbach_event_name])
        expected_len = 2
        self.assertEqual(actual_len, expected_len)

    def test_removing_listeners(self):
        event_listener = EventListener("StayAllNight")

        # Test removing events from empty list doesn't raise
        event_listener.remove_listener("doesn't exist", MagicMock)

        stay_longer_event_name = "stay a little longer"
        stay_longer_callback = MagicMock()
        event_listener.add_listener(stay_longer_event_name, stay_longer_callback)

        # Test adding 1 event
        actual_len = len(event_listener._events[stay_longer_event_name])
        expected_len = 1
        self.assertEqual(actual_len, expected_len)

        # And then removing it
        event_listener.remove_listener(stay_longer_event_name, stay_longer_callback)
        actual_len = len(event_listener._events[stay_longer_event_name])
        expected_len = 0
        self.assertEqual(actual_len, expected_len)

        # Test adding two, removing one, with the same callback
        event_listener.add_listener(stay_longer_event_name, stay_longer_callback)
        event_listener.add_listener(stay_longer_event_name, stay_longer_callback)
        event_listener.remove_listener(stay_longer_event_name, stay_longer_callback)
        actual_len = len(event_listener._events[stay_longer_event_name])
        expected_len = 1
        self.assertEqual(actual_len, expected_len)

        # Test removing all
        event_listener.remove_listener(stay_longer_event_name, stay_longer_callback)
        actual_len = len(event_listener._events[stay_longer_event_name])
        expected_len = 0
        self.assertEqual(actual_len, expected_len)

        # Test double removal doesn't raise
        event_listener.remove_listener(stay_longer_event_name, stay_longer_callback)
        actual_len = len(event_listener._events[stay_longer_event_name])
        expected_len = 0
        self.assertEqual(actual_len, expected_len)
