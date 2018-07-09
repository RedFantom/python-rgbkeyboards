"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from collections import namedtuple
from platform import architecture
import sys
# Project Modules
from rgbkeyboards.utilities import get_dll_path


PATHS = {
    "windows": {
        "Corsair": {
            "x86": "Corsair.dll",
            "x64": "Corsair64.dll"
        },
        "Cooler Master Technology Inc.": {
            "x86": "MasterKeys.dll",
            "x64": "MasterKeys64.dll"
        },
        "Logitech, Inc": {
            "x86": "Logitech.dll",
            "x64": "Logitech64.dll",
        }
    },
    "linux": {}
}

BACKENDS = {
    "windows": {
        "Corsair":
            "rgbkeyboards.windows.corsair",
        "Cooler Master Technology Inc.":
            "rgbkeyboards.windows.masterkeys",
        "Logitech, Inc.":
            "rgbkeyboards.windows.logitech"
    },
    "linux": {
        "Cooler Master Technology Inc.":
            "rgbkeyboards.linux.masterkeys",
    }
}


Device = namedtuple("Device", ["vendor", "product"])


class Keyboards(object):
    """
    Interface to control the various back-ends available

    Uses HID device interface libraries to detect devices and choose the
    correct back-end based on platform and product manufacturer.
    """

    WINDOWS = "windows"
    LINUX = "linux"

    VENDORS = [
        "Cooler Master Technology Inc.",
        "Corsair",
        "Logitech, Inc."
    ]

    def __init__(self, paths=PATHS):
        """
        :param paths: Dictionary of paths to the SDK DLL files
        """
        self.paths = PATHS
        if paths is not None:
            self.paths.update(paths)

    @property
    def platform(self):
        """Return a proper platform string across Python versions"""
        if sys.platform == "win32":
            return Keyboards.WINDOWS
        elif "linux" in sys.platform:
            return Keyboards.LINUX
        raise RuntimeError(
            "Unsupported platform detected: {}".format(sys.platform))

    def detect_devices(self):
        """Detect devices using either the Windows or Linux backend"""
        device_list = list()

        def process(vendor, product):
            if vendor not in self.VENDORS or vendor is None:
                return
            device = Device(vendor, product)
            if device in device_list:
                return
            device_list.append(device)

        # Windows
        if self.platform is Keyboards.WINDOWS:
            from pywinusb import hid
            devices = hid.HidDeviceFilter().get_devices()
            for device in devices:
                if not isinstance(device, hid.HidDevice):
                    continue
                vendor, product = device.vendor_name, device.product_name
                process(vendor, product)

        # Linux
        elif self.platform is Keyboards.LINUX:
            import usb.core
            devices = usb.core.find(find_all=True)
            for device in devices:
                try:
                    vendor, product = device.manufacturer, device.product
                except ValueError:
                    continue
                process(vendor, product)

        return device_list

    def get_backend(self, device):
        """Return the proper backend Keyboard class for a given device"""
        module = BACKENDS[self.platform][device.vendor]
        try:
            exec("from {} import Keyboard".format(module))
        except ImportError as e:
            raise RuntimeError("Failed to load back-end {}".format(module)) from e
        return locals()["Keyboard"]

    @property
    def keyboard(self):
        """Return proper Keyboard back-end instance for connected device"""
        devices = self.detect_devices()
        if len(devices) == 0:
            return None
        device = devices[0]
        return self.init_keyboard(device)

    def init_keyboard(self, device):
        """Initialize a given keyboard device"""
        Keyboard = self.get_backend(device)
        return self.init_backend(Keyboard, device)

    def init_backend(self, Keyboard, device):
        """Initialize a Keyboard class for a given device"""
        args = tuple()
        arch = "x86" if architecture()[0][:2] != "64" else "x64"
        if device.vendor in PATHS[self.platform]:
            args = (get_dll_path(PATHS[self.platform][device.vendor][arch]),)
        return Keyboard(*args)


if __name__ == '__main__':
    print(Keyboards().keyboard)
