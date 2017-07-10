# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
import unittest
from rgbkeyboards.logitech.logitech import Logitech
from rgbkeyboards.logitech.keys import keys


class TestLogitech(unittest.TestCase):
    def setUp(self):
        self.logitech = Logitech()

    def test_get_version(self):
        self.logitech.get_version()

    def test_set_control_device(self):
        self.logitech.set_control_device(Logitech.RGB_ST)

    def test_get_device_available(self):
        self.logitech.set_control_device(Logitech.RGB_ST)
        self.assertTrue(self.logitech.get_device_available())

    def test_set_full_led_color(self):
        self.logitech.set_control_device(Logitech.RGB_ST)
        self.assertTrue(self.logitech.set_led_control_enabled(True))
        self.assertTrue(self.logitech.set_full_led_color(255, 255, 255))

    def test_set_ind_led_color(self):
        self.logitech.set_control_device(Logitech.RGB_ST)
        self.logitech.set_led_control_enabled(True)
        self.assertTrue(self.logitech.set_ind_led_color({'a': (255, 0, 0)}))

    def test_get_layout(self):
        self.logitech.set_control_device(Logitech.RGB_ST)
        self.logitech.get_layout()

    def test_set_all_led_color(self):
        self.logitech.set_control_device(Logitech.RGB_ST)
        self.logitech.set_led_control_enabled(True)
        parameter = {}
        for key in keys.keys():
            parameter[key] = (255, 255, 255)
        self.assertTrue(self.logitech.set_ind_led_color(parameter))

    def tearDown(self):
        self.assertTrue(self.logitech.set_led_control_enabled(False))


if __name__ == '__main__':
    unittest.main()

