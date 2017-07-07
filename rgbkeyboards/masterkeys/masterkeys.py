# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from ctypes import c_bool, c_float, c_int, c_void_p, WINFUNCTYPE
from ctypes import cdll
from .keys import *
import platform
from ..utilities import get_dll_path


class MasterKeys(object):
    """
    This class provides a wrapper around the Cooler Master MasterKeys and MasterMouse SDK that is freely available to
    everyone. The SDK files have been included in this repository in the folder `masterkeys`, and they are required for
    the wrapper to work correctly. All functions have been wrapped, and you can use the functions just as you would
    expect to from C, but now you can call them directly from Python. Provided functionality is:
    - Setting individual key colors
    - Setting effects of the keyboard
    - Setting the colors of all keys to a single color
    - Setting the colors of all keys in one go
    - Setting and enabling a key callback
    All color-set functions can be passed integers between 0 and 255 for the red, green and blue values to make
    interfacing as easy as possible.
    """
    # Keyboard types
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

    def __init__(self, path=get_dll_path("CoolerMaster.dll"), path64=get_dll_path("CoolerMaster64.dll")):
        """
        Loads the library upon initialization and sets all the correct return types for the functions in the library
        so they can be directly read by the Python function calling the C function. Does not change the working
        directory of the program to load the library.
        """
        if int(platform.architecture()[0][:2]) == 64:
            self.library = cdll.LoadLibrary(path64)
        else:
            self.library = cdll.LoadLibrary(path)
        self.library.GetCM_SDK_DllVer.restype = c_int
        self.library.GetNowVolumePeekValue.restype = c_float
        self.library.SetControlDevice.restype = c_void_p
        self.library.IsDevicePlug.restype = c_bool
        self.library.GetDeviceLayout.restype = c_int
        self.library.EnableLedControl.restype = c_bool
        self.library.SwitchLedEffect.restype = c_bool
        self.library.RefreshLed.restype = c_bool
        self.library.SetFullLedColor.restype = c_bool
        self.library.SetAllLedColor.restype = c_bool
        self.library.EnableKeyInterrupt.restype = c_bool
        self.library.SetLedColor.restype = c_bool
        self.callback_type = WINFUNCTYPE(None, c_int, c_int, c_bool)
        self.library.SetKeyCallBack.restype = c_void_p
        self.library.SetKeyCallBack.argtypes = [self.callback_type]
        self.kb_size = 0
        self.callback = None
        self.layout = {}

    @staticmethod
    def get_brand():
        """
        Returns the brand of the keyboard in use for the universal classes
        :return: string of brand
        """
        return "coolermaster"

    def get_version(self):
        """
        Gets the version number of the SDK imported
        :return: Version number, str
        """
        return str(self.library.GetCM_SDK_DllVer())

    def get_layout(self):
        """
        Gets the layout of the keyboard
        :return: int: 0, 1 or 2, corresponding to the layout definitions above
        """
        return self.library.GetDeviceLayout()

    def get_device_available(self):
        """
        Checks if the device is ready to called upon
        :return: bool, True if ready
        """
        return self.library.IsDevicePlug()

    def set_control_device(self, device_type):
        """
        Sets the device to be controlled, corresponding to the definitions above
        :param device_type: int of device definition
                            make sure to use the device class definition instead of a plain int!
        :return: bool, True if successful
        """
        if not isinstance(device_type, int):
            raise ValueError("Device type specified is not an int, so not valid.")
        if device_type == self.RGB_L or device_type == self.WHITE_L:
            self.kb_size = 1
        elif device_type == self.RGB_M or device_type == self.WHITE_M:
            self.kb_size = 2
        elif device_type == self.RGB_S or device_type == self.WHITE_S:
            self.kb_size = 3
        else:
            raise ValueError("No valid device type")
        if self.get_layout() == self.LAYOUT_US:
            if self.kb_size == self.LARGE:
                self.layout = L_US
            elif self.kb_size == self.MEDIUM:
                self.layout = M_US
            elif self.kb_size == self.SMALL:
                self.layout = S_US
            else:
                raise ValueError("Keyboard size found not valid")
        elif self.get_layout() == self.LAYOUT_EU:
            if self.kb_size == self.LARGE:
                self.layout = L_EU
            elif self.kb_size == self.MEDIUM:
                self.layout = M_EU
            elif self.kb_size == self.SMALL:
                self.layout = S_EU
            else:
                raise ValueError("Keyboard size found not valid")
        else:
            raise ValueError("Keyboard layout found not valid")
        return self.library.SetControlDevice(device_type)

    def set_led_control_enabled(self, enable=True):
        """
        Enables or disables the connection to the device. Calling this when closing the program is mandatory to make
        sure the keyboard operations and the lighting effects return to normal!
        :param enable: bool, True to enable
        :return:
        """
        if not isinstance(enable, bool):
            raise ValueError("Parameter must be bool.")
        parameter = c_bool(enable)
        return self.library.EnableLedControl(parameter)

    def set_full_led_color(self, r, g, b):
        """
        Sets the color of all keyboard LEDs using one function
        :param r: int, 0 < r < 255
        :param g: int, 0 < g < 255
        :param b: int, 0 < b < 255
        :return:
        """
        if not -1 < r < 256 or not -1 < g < 256 or not -1 < b < 256:
            raise ValueError("Parameters must be within range 0 to 255")
        return self.library.SetFullLedColor(r, g, b)

    def set_ind_led_color(self, leds):
        """
        Set the color of an individual keyboard LED
        :param leds: dictionary of keynames with (r, g, b) tuples as values
        :return: bool, True if successful
        """
        if not isinstance(leds, dict):
            raise ValueError("Parameter leds is not a dictionary")
        if self.kb_size == self.INVALID or self.get_layout() == self.LAYOUT_DEF:
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
            self.library.SetLedColor(row, column, r, g, b)
        return True

    def set_key_callback(self, callback):
        """
        Set callback for when key is pressed. The callback must take the following arguments:
            str keyname, bool pressed
        :param callback: Callable Python object
        :return: None
        """
        self.callback = callback
        parameter = self.callback_type(self.callback_wrapper)
        self.library.SetKeyCallBack(parameter)

    def enable_key_callback(self, enable=True):
        """
        Enable the key callback when enable is True, disable when enable is False
        :param enable: bool
        :return: bool, True if successful
        """
        return self.library.EnableKeyInterrupt(enable)

    def callback_wrapper(self, row, column, pressed):
        """
        Wrapper around the callback so the name of the is returned and not the coordinates of the key, which may differ
        per keyboard.
        :param row: y coordinate, int
        :param column: x coordinate, int
        :param pressed: bool
        :return: None, calls specified callback
        """
        coordinates = (row, column)
        keyname = list(self.layout.keys())[list(self.layout.values()).index(coordinates)]
        self.callback(keyname, pressed)

    """
    The following functions are brand specific and might not be available on all keyboards. Please only use these
    functions if your are targeting a specific brand or keyboard. You can do this by letting the user enter their
    keyboard and changing the functions you call based upon that.
    """
    def get_peak_volume(self):
        """
        Gets the system volume level at the time of calling
        :return: float between 0 and 1
        """
        return self.library.GetNowVolumePeekValue()

    def refresh_leds(self):
        """
        Refreshes the LEDs manually. Currently the practical use of this function is unknown.
        :return: True if successful
        """
        return self.library.RefreshLed()

    def set_led_effect(self, effect):
        """
        Sets the keyboard lighting effect
        :param effect: int of effect definition
                       make sure to use the effect class definition instead of a plain int!
        :return: bool, True if successful
        """
        if not isinstance(effect, int):
            raise ValueError("Parameter effect is not of int type")
        return self.library.SwitchLedEffect(effect)

    def __exit__(self):
        self.enable_key_callback(False)
        self.set_led_control_enabled(False)

    def close(self):
        self.__exit__()
