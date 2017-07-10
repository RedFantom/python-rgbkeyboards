# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
import unittest
from rgbkeyboards.corsair.corsair import Corsair
from rgbkeyboards.corsair.keys import keys


class TestCorsair(unittest.TestCase):
    def setUp(self):
        self.corsair = Corsair()

    def test_get_version(self):
        self.corsair.get_version()

    def test_set_control_device(self):
        self.corsair.set_control_device()

    def test_get_device_available(self):
        self.corsair.set_control_device()
        self.assertTrue(self.corsair.get_device_available())

    def test_set_full_led_color(self):
        self.corsair.set_control_device()
        self.assertTrue(self.corsair.set_led_control_enabled(True))
        self.assertTrue(self.corsair.set_full_led_color(255, 255, 255))

    def test_set_ind_led_color(self):
        self.corsair.set_control_device()
        self.corsair.set_led_control_enabled(True)
        self.assertTrue(self.corsair.set_ind_led_color({'a': (255, 0, 0)}))

    def test_get_layout(self):
        self.corsair.set_control_device()
        self.corsair.get_layout()

    def test_set_all_led_color(self):
        self.corsair.set_control_device()
        self.corsair.set_led_control_enabled(True)
        parameter = {}
        for key in keys.keys():
            parameter[key] = (255, 255, 255)
        self.assertTrue(self.corsair.set_ind_led_color(parameter))

    def tearDown(self):
        self.assertTrue(self.corsair.set_led_control_enabled(False))


if __name__ == '__main__':
    unittest.main()
