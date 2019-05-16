from hal.relay import Relay

import unittest

class TestRelay(unittest.TestCase):

    def test_observer(self):

        def onActiveChanged(enabled: bool):
            print("relay_active={}".format(enabled))

        relay = Relay()
        relay.add_observer(onActiveChanged)
        self.assertTrue(True)
