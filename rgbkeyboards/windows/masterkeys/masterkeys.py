"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from ctypes import c_bool, c_int, c_void_p, c_byte
from ctypes import cdll
# Packages
from enum import IntEnum
# Backend Modules
from .keys import *
# Project Modules
from rgbkeyboards.keyboard import BaseKeyboard


class Keyboard(BaseKeyboard):
    """
    Windows Back-end Interface for all Cooler Master MasterKeys devices

    Relies on the official Cooler Master Custom Lighting SDK for Windows
    to control the MasterKeys keyboards.
    """
    # Keyboard types
    class KBType(IntEnum):
        RGB_L = 0
        RGB_M = 5
        RGB_S = 1
        WHITE_L = 2
        WHITE_M = 3
        WHITE_S = 7

    KB_SIZES = {
        KBType.RGB_L: L,
        KBType.RGB_M: M,
        KBType.RGB_S: S,
        KBType.WHITE_L: L,
        KBType.WHITE_M: M,
        KBType.WHITE_S: S,
    }

    def _setup_lib(self, path):
        """
        Load and initialize the library functions from an SDK DLL file
        :param path: Valid path to the library DLL file to load
        """
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
        self._layout = None

    def _get_layout(self):
        """
        Return the layout of the keyboard set to control by the library

        The GetDeviceLayout function returns an integer representing the
        layout of the connected device. Is no device is set, the
        function returns None. The layout is then matched to a layout
        dictionary using the size of the keyboard.
        """
        if self._device is None:
            return None
        r = self.library.GetDeviceLayout(self._device)
        if r == UNDEFINED:  # Library call failed
            return None
        layout = LAYOUTS[Keyboard.KB_SIZES[self._device]][r]
        return layout

    def _get_device_available(self, type=False):
        """Return the availability of any supported device"""
        for device in Keyboard.KBType:
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
        self._layout = self._get_layout()
        if self._layout is None:
            return False
        return True

    def _enable_control(self):
        """Enable control on the first available supported keyboard"""
        r = self._set_control_device()
        if r is False:  # Not device available or set device failed
            return False
        return self.library.EnableLedControl(True, self._device)

    def _disable_control(self):
        """Disable control on the currently controlled device"""
        if self._device is None:
            return False
        r = self.library.EnableLedControl(False, self._device)
        if r is True:
            self._device = None
        return r

    def _set_full_led_color(self, r, g, b):
        """
        Sets the color of all keyboard LEDs using one function

        Sets the color of all LEDs on the keyboard to the color
        specified.
        """
        if self._device is None:
            return False
        return self.library.SetFullLedColor(r, g, b, self._device)

    def _set_ind_led_color(self, leds):
        """
        Set the color of an individual keyboard LED

        Takes a dictionary with key names as keys and (r, g, b) byte
        tuples as values. Keys that are not in the dictionary do not
        change color.
        # TODO: Implement support for SetAllLedColor with matrix
        """
        for key, value in leds.items():
            if self._layout[key] is None:
                continue
            row, column = self._layout[key]
            r, g, b = value
            r = self.library.SetLedColor(row, column, r, g, b, self._device)
            if r is False:
                return False
        return True

    @staticmethod
    def is_product_supported(product):
        """
        Determine if a product is supported based on USB product string

        For Cooler Master devices, the situation is a bit
        complicated, because Cooler Master uses non-unique iProduct USB
        descriptor strings for RGB and non-RGB supporting devices. Only
        if the device has three Endpoints does the device support
        lighting control. That is what is checked using this function,
        but that does make it pretty slow.
        """
        from pywinusb import hid
        devices = hid.HidDeviceFilter().get_devices()
        count = 0
        for device in devices:
            if not isinstance(device, hid.HidDevice):
                continue
            if device.product_name == product:
                count += 1
        return count == 3
