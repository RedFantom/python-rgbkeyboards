"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from ctypes import c_bool, c_int, c_void_p, c_byte
from ctypes import cdll
from pywinusb import hid
# Packages
from enum import Enum
# Project Modules
from .keys import *


class Keyboard(object):
    """
    Windows Back-end Interface for all Cooler Master MasterKeys devices
    """
    # Keyboard types
    class KeyboardType(Enum):
        RGB_L = 0
        RGB_M = 5
        RGB_S = 1
        WHITE_L = 2
        WHITE_M = 3
        WHITE_S = 7

    # Keyboard sizes
    INVALID = 0
    LARGE = 1
    MEDIUM = 2
    SMALL = 3

    # Lay-out types
    LAYOUT_DEF = 0
    LAYOUT_US = 1
    LAYOUT_EU = 2
    LAYOUT_JP = 3

    # LED Effects
    EFF_FULL_ON = 0
    EFF_BREATH = 1
    EFF_BREATH_CYCLE = 2
    EFF_SINGLE = 3
    EFF_WAVE = 4
    EFF_RIPPLE = 5,
    EFF_CROSS = 6
    EFF_RAIN = 7
    EFF_STAR = 8
    EFF_SNAKE = 9
    EFF_REC = 10,
    EFF_SPECTRUM = 11
    EFF_RAPID_FIRE = 12
    # Mouse effect only, currently not used
    EFF_INDICATOR = 13

    # These are multi effects
    # The values appear to be memory addresses of the chip in the keyboard
    # Currently not tested
    EFF_MULTI_1 = 0xE0
    EFF_MULTI_2 = 0xE1
    EFF_MULTI_3 = 0xE2
    EFF_MULTI_4 = 0xE3
    EFF_OFF = 0xFE

    def __init__(self, path):
        """
        Load the library and initialize the ctypes functions
        :param path: Valid path to the library DLL file to load
        """
        print(path)
        self.library = lib = cdll.LoadLibrary(path)

        # void SetControlDevice(DEVICE_INDEX)
        lib.SetControlDevice.restype = c_void_p
        lib.SetControlDevice.argtypes = [c_int]
        # bool IsDevicePlug(DEVICE_INDEX)
        lib.IsDevicePlug.restype = c_bool
        lib.IsDevicePlug.argtypes = [c_int]
        # LAYOUT_KEYBOARD GetDeviceLayout(DEVICE_INDEX)
        lib.GetDeviceLayout.argtypes = [c_int]
        lib.GetDeviceLayout.restype = c_int
        # bool EnableLedControl(bool, DEVICE_INDEX)
        lib.EnableLedControl.restype = c_bool
        lib.EnableLedControl.argtypes = [c_bool, c_int]
        # bool SwitchLedEffect(EFF_INDEX, DEVICE_INDEX)
        lib.SwitchLedEffect.restype = c_bool
        lib.SwitchLedEffect.argtypes = [c_int, c_int]
        # bool RefreshLed(bool, DEVICE_INDEX)
        lib.RefreshLed.restype = c_bool
        lib.RefreshLed.argtypes = [c_bool, c_int]
        # bool SetFullLedColor(BYTE, BYTE, BYTE, DEVICE_INDEX)
        lib.SetFullLedColor.restype = c_bool
        lib.SetFullLedColor.argtypes = [c_byte, c_byte, c_byte, c_int]
        # bool SetAllLedColor(COLOR_MATRIX, DEVICE_INDEX)
        lib.SetAllLedColor.restype = c_bool
        # TODO: Implement COLOR_MATRIX in ctypes
        # bool SetLedColor(int, int, BYTE, BYTE, BYTE, DEVICE_INDEX)
        lib.SetLedColor.restype = c_bool
        lib.SetLedColor.argtypes = [c_int, c_int, c_byte, c_byte, c_byte, c_int]

        self._device = None
        self.layout = None
        self._control = False

    def _get_layout(self):
        """
        Return the layout of the keyboard

        Return an integer representing a keyboard layout in the
        library.
        # TODO: Implement automatic layout detection for setting all leds
        """
        return self.library.GetDeviceLayout(0xFFFF)

    def get_device_available(self, type=False):
        """Return the availability of any supported device"""
        for device in Keyboard.KeyboardType:
            r = self.library.IsDevicePlug(device)
            if r is True:
                return True if type is False else device
        return False if type is False else None

    def _set_control_device(self):
        """Select the first encountered keyboard for control"""
        available_dev = self.get_device_available(True)
        if available_dev is None:
            return False
        r = self.library.SetControlDevice(available_dev)
        if r is False:
            return False
        self._device = available_dev
        return True

    def enable_control(self):
        """Enable control on the first available supported keyboard"""
        r = self._set_control_device()
        if r is False:  # Not device available or set device failed
            return False
        r = self.library.EnableControl(True, self._device)
        if r is True:
            self._control = True
        return r

    def disable_control(self):
        """Disable control on the currently controlled device"""
        if self._device is None:
            return False
        r = self.library.EnableControl(False, self._device)
        if r is False:
            return False
        self._device = None
        self._control = False
        return True

    def set_full_led_color(self, r, g, b):
        """
        Sets the color of all keyboard LEDs using one function

        Sets the color of all LEDs on the keyboard to the color
        specified.
        """
        if self._device is None:
            return
        if not all(-1 < v < 256 for v in (r, g, b)):
            raise ValueError("Parameters must be within range 0 to 255")
        return self.library.SetFullLedColor(r, g, b, self._device)

    def set_ind_led_color(self, leds):
        """
        Set the color of an individual keyboard LED

        Takes a dictionary with key names as keys and (r, g, b) byte
        tuples as values. Keys that are not in the dictionary do not
        change color.
        # TODO: Implement support for SetAllLedColor with matrix
        """
        if not isinstance(leds, dict):
            raise ValueError("Parameter leds is not a dictionary")
        if self.kb_size == self.INVALID or self._get_layout() == self.LAYOUT_DEF:
            raise ValueError("Control device not set")
        for key, value in leds.items():
            if key not in self.layout:
                raise ValueError("Invalid key found")
            if not isinstance(value, tuple):
                raise ValueError("Value found for key not tuple")
            if not len(value) == 3:
                raise ValueError("Value found for key not with length 3")
            if not self.layout[key]:
                continue
            row, column = self.layout[key]
            r, g, b = value
            self.library.SetLedColor(row, column, r, g, b, 0xFFFF)
        return True

    def __exit__(self):
        if not self._control:
            return
        self.set_led_control_enabled(False)

    """
    These functions are platform specific
    """

    def refresh_leds(self):
        """
        Flushes key colors still in memory to the keyboard

        The library runs a separate Thread to asynchronously send the
        packets to the keyboard. While the documentation is sketchy, it
        would appear that this function synchronously flushes the cache.
        Under normal circumstances, this function should not be
        necessary.
        """
        return self.library.RefreshLed(self._device)
