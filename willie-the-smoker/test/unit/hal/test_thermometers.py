from hal.thermometers import Thermometers

import unittest


class TestThermometers(unittest.TestCase):

    def test_to_f(self):

        thermometers = Thermometers()

        actual_temp = thermometers._to_f(0)
        expected_temp = 32.0
        self.assertEqual(actual_temp, expected_temp)

        actual_temp = thermometers._to_f(100)
        expected_temp = 212.0
        self.assertEqual(actual_temp, expected_temp)

        actual_temp = thermometers._to_f(121.111)
        expected_temp = 250.0
        self.assertAlmostEqual(actual_temp, expected_temp, places=1)
