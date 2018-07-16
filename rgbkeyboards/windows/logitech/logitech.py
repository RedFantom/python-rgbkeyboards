"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from ctypes import cdll, c_bool, c_int
# Backend Modules
from . import keys
# Project Modules
from rgbkeyboards.keyboard import BaseKeyboard
from rgbkeyboards.utilities import get_device_list

_MODELS = [
    # Not all models in the list support per-key RGB lighting
    # Monochrome devices use the maximum of the color tuple as brightness
    # Some monochrome devices do not support the full 100-level resolution
    # Per-key RGB commands are ignored when they are not supported
    "G910",
    "G810",
    "G710+",
    "G610",
    "G510",
    "G110",
    "G105",
    "G11",
    "G15"
]


class Keyboard(BaseKeyboard):
    """
    Windows back-end interface to the Logitech keyboards

    Uses the LogiLed SDK DLL files to control the Logitech keyboards.
    The SDK has to be in the file provided upon class initialization.
    Note that the SDK DLL file depends on the Logitech Gaming Software.
    """

    VENDOR = "Logitech, Inc."

    def _setup_lib(self, path):
        """Load and initialize library function from DLL"""
        self._library = lib = cdll.LoadLibrary(path)
        self._init = False
        # bool LogiLedInit()
        lib.LogiLedInit.restype = c_bool
        # bool LogiLedSetTargetDevice(int targetDevice)
        lib.LogiLedSetTargetDevice.restype = c_bool
        lib.LogiLedSetTargetDevice.argtypes = [c_int]
        # bool LogiLedSetLighting(int r, int g, int b)
        lib.LogiLedSetLighting.restype = c_bool
        lib.LogiLedSetLighting.argtypes = [c_int, c_int, c_int]
        # bool LogiLedSetLightingForKeyWithKeyName(
        #    enum KeyName keyName, int r, int g, int b)
        lib.LogiLedSetLightingForKeyWithKeyName.restype = c_bool
        lib.LogiLedSetLightingForKeyWithKeyName.argtypes = [c_int] * 4
        # bool LogiLedShutdown()
        lib.LogiLedShutdown.restype = c_bool

    def _get_device_available(self):
        """
        Return whether any supported device is connected

        The LogiLed library actually does not allow direct access to the
        keyboards, thus the keyboards have to be detected in a more
        complicated manner.
        """
        devices = get_device_list([Keyboard.VENDOR])
        if len(devices) == 0:
            return False
        return any(self.is_product_supported(product) for _, product in devices)

    def _enable_control(self):
        """Enable control by initializing LogiLed connection"""
        return self._library.LogiLedInit()

    def _disable_control(self):
        """Disable control by closing the LogiLed connection"""
        return self._library.LogiLedShutdown()

    def _set_full_led_color(self, r, g, b):
        """Set the color of all the LEDs on the keyboard"""
        r, g, b = map(self._scale, (r, g, b))
        return self._library.LogiLedSetLighting(r, g, b)

    def _set_ind_led_color(self, leds):
        """
        Set the colors of individual LEDs on the keyboard

        Note that this function does not use the
        LogiLedSetLightingWithBitmap library function because its
        behaviour is inconsistent across devices (the matrix has
        different keys in the same coordinates across layouts).
        """
        for keyname, (r, g, b) in leds.items():
            r, g, b = map(self._scale, (r, g, b))
            keycode = keys.keys[keyname]
            if not keycode:
                continue
            result = self._library.LogiLedSetLightingWithKeyName(keycode, r, g, b)
            if result is False:
                return False
        return True

    @staticmethod
    def is_product_supported(product):
        """Determine whether a product is supported based on product string"""
        return any(k in product for k in _MODELS)

    @staticmethod
    def _scale(v):
        """Scale the value from 0-255 to 0-100 for LogiLed library"""
        return int(v * 100 / 255)
