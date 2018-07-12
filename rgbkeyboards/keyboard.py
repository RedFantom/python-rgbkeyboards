"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""


class BaseKeyboard(object):
    """
    Defines the interface described in BACKENDS.md

    :attribute _control: Flag to be set to True when keyboard control is
        enabled. Should only be set after successfully enabling keyboard
        control, so only after error checking.
    """

    def enable_control(self):
        """Enable control on the first found supported keyboard"""
        raise NotImplementedError()

    def disable_control(self):
        """Disable control on the controlled keyboard"""
        raise NotImplementedError()

    def set_full_led_color(self, r, g, b):
        """Set the keyboard of all the LEDs of the keyboard"""
        raise NotImplementedError()

    def set_ind_led_color(self, leds):
        """Set the color of all LEDs on the keyboard individually"""
        raise NotImplementedError()

    def get_device_available(self):
        """Return whether a supported device is available"""
        raise NotImplementedError()

    def __enter__(self):
        """Allows class to be used in with-clause"""
        if self.get_device_available() is False:
            raise RuntimeError("No available device found")
        self.enable_control()
        if self._control is False:
            raise RuntimeError("Failed to enable control on keyboard")
        return self

    def __exit__(self, *args):
        """Disable control at end of with-clause"""
        if self._control:
            return
        self.disable_control()

    @staticmethod
    def is_product_supported(product):
        """Return whether a product is supported by iProduct USB string"""
        raise NotImplementedError()
