# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from ctypes import c_bool, c_int, c_void_p
from ctypes import cdll
import platform
from ..utilities import get_dll_path
from ..keyboard import Keyboard


class Razer(Keyboard):

    # Based on the MasterKeys effects
    # The other effects for Razer are currently not available
    EFF_FULL_ON = 4
    EFF_BREATH = 1
    EFF_WAVE = 6
    EFF_SPECTRUM = 5

    def __init__(self, path=get_dll_path("Razer.dll"), path64=get_dll_path("Razer64.dll")):
        if int(platform.architecture()[0][:2]) == 64:
            self._library = cdll.LoadLibrary(path64)
        else:
            self._library = cdll.LoadLibrary(path)
        self._library.CreateKeyboardEffect.argtypes = [c_int]
        self.__init = False

    @staticmethod
    def get_brand():
        return "razer"

    def get_version(self):
        return "1.0.0"

    def get_layout(self):
        return 0

    def get_device_available(self):
        return self.__init

    def set_control_device(self, device_type=0):
        if self.__init:
            return True
        else:
            return False

    def set_led_control_enabled(self, enable=True):
        if enable:
            self._library.Init()
            self.__init = True
        else:
            self._library.UnInit()
            self.__init = False

    def set_full_led_color(self, r, g, b):
        return

    def set_ind_led_color(self, leds):
        return

    def close(self):
        self._library.UnInit()
        self.__init = False

    def __exit__(self):
        self.close()
