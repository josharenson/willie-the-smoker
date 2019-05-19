from common.events import RELAY_ACTIVE
from hal.relay import Relay

from unittest.mock import MagicMock
import unittest


class TestRelay(unittest.TestCase):

    def test_observer(self):

        onActiveChanged = MagicMock()

        relay = Relay()
        relay.add_observer(RELAY_ACTIVE, onActiveChanged)
        relay.active = True
        onActiveChanged.assert_called_with(True)

        relay.active = False
        onActiveChanged.assert_called_with(False)

        self.assertFalse(relay.active)
