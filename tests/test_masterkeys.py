# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
import unittest
from rgbkeyboards.masterkeys.masterkeys import MasterKeys
import rgbkeyboards.masterkeys.keys as mkkeys


class TestMasterKeys(unittest.TestCase):
    """
    Contains the tests for the MasterKeys class in the masterkeys.py file. Runs tests on all functions, based upon the
    Cooler Master MasterKeys Pro L RGB keyboard. This can be changed by changing the class definition.
    """
    def setUp(self):
        self.masterkeys = MasterKeys()

    def test_get_version(self):
        self.masterkeys.get_version()

    def test_set_control_device(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)

    def test_get_device_available(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)
        self.assertTrue(self.masterkeys.get_device_available())

    def test_set_full_led_color(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)
        self.assertTrue(self.masterkeys.set_led_control_enabled(True))
        self.assertTrue(self.masterkeys.set_full_led_color(255, 255, 255))

    def test_set_ind_led_color(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)
        self.masterkeys.set_led_control_enabled(True)
        self.assertTrue(self.masterkeys.set_ind_led_color({'a': (255, 0, 0)}))

    def test_set_led_effect(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)
        self.masterkeys.set_led_control_enabled(True)
        self.assertTrue(self.masterkeys.set_led_effect(MasterKeys.EFF_BREATH))
        self.assertTrue(self.masterkeys.set_led_effect(MasterKeys.EFF_FULL_ON))

    def test_get_layout(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)
        self.masterkeys.get_layout()

    def test_set_all_led_color(self):
        self.masterkeys.set_control_device(MasterKeys.RGB_L)
        self.masterkeys.set_led_control_enabled(True)
        parameter = {}
        for key in mkkeys.L_US.keys():
            parameter[key] = (255, 255, 255)
        self.assertTrue(self.masterkeys.set_ind_led_color(parameter))

    def tearDown(self):
        self.assertTrue(self.masterkeys.set_led_control_enabled(False))


if __name__ == '__main__':
    unittest.main()
