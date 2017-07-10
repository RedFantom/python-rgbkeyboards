# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from .keys import *
from . import defs
from ctypes import cdll, c_bool
from platform import architecture
import os
from ..utilities import get_dll_path
from ..keyboard import Keyboard


class Logitech(Keyboard):
    RGB_ST = defs.LOGI_DEVICETYPE_RGB
    RGB_PK = defs.LOGI_DEVICETYPE_PERKEY_RGB
    WHITE = defs.LOGI_DEVICETYPE_MONOCHROME

    def __init__(self, path=get_dll_path("Logitech.dll"), path64=get_dll_path("Logitech64.dll")):
        self._path = path64 if int(architecture()[0][:2]) == 64 else path
        if not os.path.exists(self._path):
            raise FileNotFoundError
        self._library = cdll.LoadLibrary(self._path)
        self._library.LogiLedInit.restype = c_bool
        self._library.LogiLedSetTargetDevice.restype = c_bool
        self._library.LogiLedSaveCurrentLighting.restype = c_bool
        self._library.LogiLedRestoreLighting.restype = c_bool
        self._library.LogiLedSetLighting.restype = c_bool
        self._library.LogiLedFlashLighting.restype = c_bool
        self._library.LogiLedPulseLighting.restype = c_bool
        self._library.LogiLedStopEffects.restype = c_bool
        self._library.LogiLedSetLightingForKeyWithScanCode.restype = c_bool
        self._library.LogiLedSetLightingForKeyWithHidCode.restype = c_bool
        self._library.LogiLedSetLightingForKeyWithQuartzCode.restype = c_bool
        self._library.LogiLedSetLightingForKeyWithKeyName.restype = c_bool
        self._library.LogiLedSaveLightingForKey.restype = c_bool
        self._library.LogiLedRestoreLightingForKey.restype = c_bool
        self._library.LogiLedFlashLighting.restype = c_bool
        self._library.LogiLedPulseLighting.restype = c_bool
        self._library.LogiLedStopEffectsOnKey.restype = c_bool
        self._library.LogiLedShutdown.restype = c_bool
        # self._library.LogiLedGetSdkVersion
        self._callback = None
        self._listener = None

    @staticmethod
    def get_brand():
        return "logitech"

    def get_version(self):
        return self._library.LogiLedGetSdkVersion()

    def get_layout(self):
        """
        Not available for the LogiLed SDK, but gracefully returns 0
        :return:
        """
        return 0

    def get_device_available(self):
        return self._library.LogiLedInit()

    def set_control_device(self, device_type):
        if not isinstance(device_type, int):
            raise ValueError("Parameter is not of int type")
        if not device_type == Logitech.RGB_ST and not device_type == Logitech.RGB_PK and \
           not device_type == Logitech.WHITE:
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
