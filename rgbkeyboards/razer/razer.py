# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from ..keyboard import Keyboard
from ..sdks import ChromaPy as chroma
from .keys import keys


class Razer(Keyboard):

    # Based on the MasterKeys effects
    # The other effects for Razer are currently not available
    EFF_FULL_ON = 4
    EFF_BREATH = 1
    EFF_WAVE = 6
    EFF_SPECTRUM = 5

    def __init__(self):
        self.__init = False
        self._library = chroma.Keyboard()

    @staticmethod
    def get_brand():
        return "razer"

    def get_version(self):
        return "1.0.0"

    def get_layout(self):
        return 0

    def get_device_available(self):
        return bool(chroma.getConnectedDevices())

    def set_control_device(self, device_type=0):
        if self.__init:
            return True
        else:
            return False

    def set_led_control_enabled(self, enable=True):
        return True

    def set_full_led_color(self, r, g, b):
        return self._library.setColor((r, g, b))

    def set_ind_led_color(self, leds):
        for led, value in leds:
            try:
                self._library.setbyGrid(keys[led][value])
            except KeyError:
                raise ValueError("This key is not valid for this keyboard: {0}".format(led))
            except SyntaxError:
                pass
        return self._library.applyEffectKeyboard()

    def close(self):
        self.__init = False

    def __exit__(self):
        self.close()
