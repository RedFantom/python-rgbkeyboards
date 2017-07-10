# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE


class Keyboard(object):
    @staticmethod
    def get_brand():
        raise NotImplementedError

    def get_version(self):
        raise NotImplementedError

    def get_layout(self):
        raise NotImplementedError

    def get_device_available(self):
        raise NotImplementedError

    def set_control_device(self, device_type):
        raise NotImplementedError

    def set_led_control_enabled(self, enable=True):
        raise NotImplementedError

    def set_full_led_color(self, r, g, b):
        raise NotImplementedError

    def set_ind_led_color(self, leds):
        raise NotImplementedError
