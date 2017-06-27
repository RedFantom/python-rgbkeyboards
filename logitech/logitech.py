# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from .logipy import logi_led as library
from .keys import *
from pynput import keyboard as kb


class Logitech(object):
    RGB_ST = library.LOGI_DEVICETYPE_RGB
    RGB_PK = library.LOGI_DEVICETYPE_PERKEY_RGB
    WHITE = library.LOGI_DEVICETYPE_MONOCHROME

    def __init__(self):
        if not library.logi_led_init():
            raise ValueError("Logitech library could not be initialized")
        self._callback = None
        self._listener = None

    @staticmethod
    def get_brand():
        return "logitech"

    @staticmethod
    def get_version():
        return library.get_sdk_version()

    @staticmethod
    def get_layout():
        return 0

    @staticmethod
    def get_device_available():
        return True

    @staticmethod
    def set_control_device(device_type):
        if not isinstance(device_type, int):
            raise ValueError("Parameter is not of int type")
        if not device_type == Logitech.RGB_ST or not device_type == Logitech.RGB_PK or \
           not device_type == Logitech.WHITE:
            raise ValueError("Parameter is not a valid device type")
        return library.logi_led_set_target_device(device_type)

    @staticmethod
    def set_led_control_enabled():
        """
        Funtion is not required for Logitech SDK
        :return: True
        """
        return True

    @staticmethod
    def set_full_led_color(r, g, b):
        r = int(r / 255 * 100)
        g = int(g / 255 * 100)
        b = int(b / 255 * 100)
        library.logi_led_set_lighting(r, g, b)

    @staticmethod
    def set_ind_led_color(leds):
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
            library.logi_led_set_lighting_for_key_with_scan_code(keycode, r, g, b)
        return True

    def set_key_callback(self, callback):
        self._callback = callback
        self._listener = kb.Listener(on_press=self._callback)

    def enable_key_callback(self, enable=True):
        if not self._callback or not callable(self._callback):
            raise ValueError("Callback not set. Please use set_key_callback")
        if not self._listener or not isinstance(self._listener, kb.Listener):
            raise ValueError("Callback set but listener not found")
        if enable:
            self._listener.start()
        else:
            self._listener.stop()
            while self._listener.is_alive():
                pass
            return

    def close(self):
        self.__exit__()

    def __exit__(self):
        library.logi_led_shutdown()
