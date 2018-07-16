"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
import logging
# Backend Modules
from rgbkeyboards.windows.masterkeys.keys import \
    LAYOUTS, L, M, S, US, EU
# Project Modules
from rgbkeyboards.keyboard import BaseKeyboard


DEVICE_LAYOUTS = {
    # TODO: Complete this list with more data
    0x003b: (L, US),
    0x0047: (L, EU),
}


SUCCESS = 0


class Keyboard(BaseKeyboard):
    """
    Wrapper around the masterkeys package for Linux

    The MasterKeys package is based on libmk and still depends on the
    key coordinates. On Linux, it is difficult to determine the layout
    of a keyboard, especially as the MasterKeys devices do not identify
    even whether they support lighting effects using USB descriptors.
    """

    VENDOR = "Cooler Master Technology Inc."

    def _setup_lib(self):
        """Load masterkeys module and initialize required attributes"""
        import masterkeys as mk
        self._library = mk
        self._layout = None
        self._size = None
        self._lighting = mk.build_layout_list()
        global SUCCESS
        SUCCESS = mk.SUCCESS

    def _get_device_available(self):
        """Return whether any supported device is available"""
        devices = self._library.detect_devices()
        return len(devices) != 0

    def _enable_control(self):
        """Enable control of the first keyboard detected"""
        devices = self._library.detect_devices()
        r = self._library.set_device(devices[0])
        if r != SUCCESS:
            return False
        r = self._library.enable_control()
        if r != SUCCESS:
            return False
        self._control = True
        self._size, self._layout = self._get_layout()
        return True

    def _disable_control(self):
        """Disable control on the controlled keyboard"""
        r = self._library.disable_control()
        if r != SUCCESS:
            return False
        self._size, self._layout = None, None
        return True

    def _get_layout(self):
        """Return the layout and size for the controlled device"""
        device = self._library.get_device_ident()
        if device not in DEVICE_LAYOUTS:
            return None, None
        return DEVICE_LAYOUTS[device]

    def _set_full_led_color(self, r, g, b):
        """Set the color of LEDs on the keyboard"""
        return self._library.set_full_led_color(r, g, b)

    def _set_ind_led_color(self, leds):
        """Set the color of individual LEDs"""
        if self._size is None or self._layout is None:
            device = self._library.get_device_ident()
            logging.info("[MasterKeys RGB Keyboard Backend] "
                         "Unknown layout for device {}. Please report "
                         "this in the GitHub repository.".format(device))
            return False
        layout = LAYOUTS[self._size][self._layout]
        for name, (r, g, b) in leds.items():
            coords = layout[name]
            if coords is None:
                continue
            r, c = coords
            self._lighting[r][c] = (r, g, b)
        return self._library.set_all_led_color(self._lighting) == SUCCESS

    @staticmethod
    def is_product_supported(product):
        """
        Determine whether a product is supported with USB iProduct

        Due to the limitations of the libmk library limitations, this
        function only checks whether the keyboard is a MasterKeys
        device with three HID Interfaces.
        """
        import usb.core
        devices = usb.core.find(find_all=True)
        for device in devices:
            try:
                is_vendor = device.manufacturer == Keyboard.VENDOR
                is_product = device.product == product
            except ValueError:
                continue
            if not is_vendor or not is_product:
                continue
            config = device.get_active_configuration()
            return config.bNumInterfaces == 3
        return False
