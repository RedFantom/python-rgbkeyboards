"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Packages
from cue_sdk.api import *
from cue_sdk.structures import *
from cue_sdk.enumerations import *
# Backend Modules
from .keys import *
# Project Modules
from rgbkeyboards.keyboard import BaseKeyboard


class Keyboard(BaseKeyboard):
    """
    Back-end for Corsair keyboards based on the Python wrapper cue_sdk

    Relies on the cue_sdk Python wrapper of the Corsair CUE SDK DLL
    file. cue_sdk uses ctypes to handle the CUE SDK DLL file.
    """

    def _setup_lib(self, path):
        """Initialize CUESDK instance with DLL path"""
        self._library = CUESDK(path, silence_errors=True)

    def _get_device_available(self):
        """Return the availability of any supported device"""
        return self._library.GetDeviceCount() > 0

    def _enable_control(self):
        """Enable exclusive lighting control for a Corsair keyboard"""
        return self._library.request_control(CAM.ExclusiveLightingControl)

    def _disable_control(self):
        """Disable exclusive lighting control for controlled keyboard"""
        return self._library.release_control(CAM.ExclusiveLightingControl)

    def _set_full_color(self, r, g, b):
        """Set the color of all the LEDs on the controlled keyboard"""
        return self._library.set_led_colors(
            [CorsairLedColor(i, r, g, b) for i in keys.values()])

    def _set_ind_color(self, leds):
        """
        Sets the colors of individual LEDs by keyname
        :param leds: dictionary with keynames as key and tuples (r, g, b) as values
        :return:
        """
        parameter = []
        for key, value in leds.items():
            if keys[key] is None:
                return
            (r, g, b) = value
            parameter.append(CorsairLedColor(keys[key], r, g, b))
        return self._library.set_led_colors(parameter)

    @staticmethod
    def is_product_supported(product):
        """Determine whether a product is supported based on USB string"""
        return "RGB" in product
