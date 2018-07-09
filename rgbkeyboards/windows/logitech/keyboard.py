"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from .keys import *
from . import defs
from ctypes import cdll, c_bool


class Keyboard(object):
    """
    Windows back-end interface to the Logitech keyboards

    Uses the LogiLed SDK DLL files to control the Logitech keyboards.
    The SDK has to be in the file provided upon class initialization.
    """

    RGB_ST = defs.LOGI_DEVICETYPE_RGB
    RGB_PK = defs.LOGI_DEVICETYPE_PERKEY_RGB
    WHITE = defs.LOGI_DEVICETYPE_MONOCHROME

    def __init__(self, path):
        """
        Load the library and initialize the ctypes functions
        :param path: Full path to the library DLL file
        """
        self._library = lib = cdll.LoadLibrary(path)
        lib.LogiLedInit.restype = c_bool
        lib.LogiLedSetTargetDevice.restype = c_bool
        lib.LogiLedSaveCurrentLighting.restype = c_bool
        lib.LogiLedRestoreLighting.restype = c_bool
        lib.LogiLedSetLighting.restype = c_bool
        lib.LogiLedFlashLighting.restype = c_bool
        lib.LogiLedPulseLighting.restype = c_bool
        lib.LogiLedStopEffects.restype = c_bool
        lib.LogiLedSetLightingForKeyWithScanCode.restype = c_bool
        lib.LogiLedSetLightingForKeyWithHidCode.restype = c_bool
        lib.LogiLedSetLightingForKeyWithQuartzCode.restype = c_bool
        lib.LogiLedSetLightingForKeyWithKeyName.restype = c_bool
        lib.LogiLedSaveLightingForKey.restype = c_bool
        lib.LogiLedRestoreLightingForKey.restype = c_bool
        lib.LogiLedFlashLighting.restype = c_bool
        lib.LogiLedPulseLighting.restype = c_bool
        lib.LogiLedStopEffectsOnKey.restype = c_bool
        lib.LogiLedShutdown.restype = c_bool
        self._callback = None
        self._listener = None

    def get_device_available(self):
        """Return the availability of a Logitech keyboard device"""
        return self._library.LogiLedInit()

    def set_control_device(self, device_type):
        if not isinstance(device_type, int):
            raise ValueError("Parameter is not of int type")
        if not device_type == Keyboard.RGB_ST and not device_type == Keyboard.RGB_PK and \
           not device_type == Keyboard.WHITE:
            raise ValueError("Parameter is not a valid device type")
        self._library.LogiLedSetTargetDevice(device_type)

    def set_led_control_enabled(self, enabled=True):
        if not enabled:
            return False
        return self._library.LogiLedInit()

    def set_full_led_color(self, r, g, b):
        r = int(r / 255 * 100)
        g = int(g / 255 * 100)
        b = int(b / 255 * 100)
        self._library.LogiLedSetLighting(r, g, b)

    def set_ind_led_color(self, leds):
        if not isinstance(leds, dict):
            raise ValueError("Parameter leds is not a dictionary")
        for key, value in leds.items():
            if key not in keys:
                raise ValueError("Invalid key found")
            if not isinstance(value, tuple):
                raise ValueError("Value found for key not tuple")
            if not len(value) == 3:
                raise ValueError("Value found for key not with length 3")
            r = int(value[0] / 255 * 100)
            g = int(value[1] / 255 * 100)
            b = int(value[2] / 255 * 100)
            keycode = keys[key]
            if not keycode:
                continue
            return_value = self._library.LogiLedSetLightingForKeyWithScanCode(keycode, r, g, b)
            if not return_value:
                return False
        return True

    def close(self):
        self._library.LogiLedShutdown()

    def __exit__(self):
        self.close()
