"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
import logging
# Project Modules
from rgbkeyboards.keyboard import BaseKeyboard

_DEVICES = [
    "Razer BlackWidow Ultimate 2012",
    "Razer BlackWidow Classic ",
    "Razer Anansi",
    "Razer BlackWidow Ultimate 2013",
    "Razer BlackWidow Stealth",
    "Razer DeathStalker Expert",
    "Razer BlackWidow Chroma",
    "Razer DeathStalker Chroma",
    "Razer Blade Stealth",
    "Razer Orbweaver Chroma",
    "Razer BlackWidow Tournament Edition Chroma",
    "Razer Blade QHD",
    "Razer Blade Pro ",
    "Razer BlackWidow Chroma ",
    "Razer BlackWidow Ultimate 2016",
    "Razer BlackWidow X Chroma",
    "Razer BlackWidow X Ultimate",
    "Razer BlackWidow X Tournament Edition Chroma",
    "Razer Ornata Chroma",
    "Razer Ornata",
    "Razer Blade Stealth ",
    "Razer BlackWidow Chroma V2",
    "Razer Blade ",
    "Razer Cynosa Chroma",
    "Razer Blade Stealth ",
    "Razer Blade Pro ",
    "Razer Blade Pro FullHD ",
    "Razer Blade Stealth ",
    "Razer Blade 15 ",
    "Razer Blade 15 Mercury",
]


class Keyboard(BaseKeyboard):
    """
    Wrapper around openrazer Python Library

    The openrazer project provides open source kernel drivers for many
    Razer keyboards. Communication happens through DBus, but all of that
    is abstracted away in the Python library.

    In order for this back-end to be used, openrazer must be installed
    per installation instructions, which can be found in the README of
    the project: <github.com/openrazer/openrazer>

    Due to type-hinting, the Python Library of openrazer is only
    compatible with Python 3.5 and up.
    """

    def _setup_lib(self):
        """Initialize the library"""
        try:
            from openrazer.client import DeviceManager
        except ImportError:  # The library is not available
            print("Please install the openrazer package for your platform")
            raise
        except SyntaxError:
            print("The openrazer Python library only supports Python 3.5+")
            raise
        self._lib = DeviceManager()
        self._device = None

    def _get_device_available(self):
        """Return whether any supported device is available"""
        devices = self._lib.devices
        return len(devices) != 0

    def _enable_control(self):
        """Enable control of the first keyboard detected"""
        devices = self._lib.devices
        if len(devices) == 0:
            return False
        self._device = devices[0]
        return True

    def _disable_control(self):
        """Disable control on the controlled keyboard"""
        self._device = None
        return True

    def _set_full_color(self, r, g, b):
        """Set the color of all LEDs on the keyboard"""
        if self._device is None:
            return False
        return self._device.fx.static(r, g, b)  # bool

    def _set_ind_color(self, leds):
        """Set the color of individual LEDs"""
        # TODO: Implement support for individual LED control
        # Notes:
        # Can be implemented using the RazerAdvancedFX class function
        # set_key(column: int, rgb: Tuple[int, int, int], row: int)
        # Requires layout support due to row/column system: row/columns
        # must be mapped to key names as with masterkeys backends
        return False

    @staticmethod
    def is_product_supported(product):
        """
        Return whether a product is supported by the library

        Device support depends on the underlying openrazer kernel
        drivers, and can thus change. Whether a device is actually
        supported can only be determined by checking whether a device
        is available through the DeviceManager().devices property.

        However, if this function is called, the library is not imported
        and initialized yet, and thus whether a specific device is
        supported can only be checked statically.

        Therefore, the product name string is checked against a list
        of supported devices taken from the README of the project.
        """
        return product in _DEVICES
