"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from platform import architecture
import sys
# Project Modules
from rgbkeyboards.utilities import \
    WINDOWS, LINUX, get_dll_path, get_device_list


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

VENDORS = list(BACKENDS[WINDOWS].keys())


def register_backend(platform, vendor, module, dlls=None):
    """Register a new backend for a certain set of keyboards"""
    if platform not in (LINUX, WINDOWS):
        raise ValueError("Invalid platform value")
    BACKENDS[platform][vendor] = module
    if dlls is not None:
        assert isinstance(dlls, dict)
        if "x86" not in dlls or "x64" not in dlls:
            raise ValueError("Invalid dlls dictionary")
        PATHS[platform][vendor] = dlls
    return True


class Keyboards(object):
    """
    Interface to control the various back-ends available

    Uses HID device interface libraries to detect devices and choose the
    correct back-end based on platform and product manufacturer.
    """

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
            return WINDOWS
        elif "linux" in sys.platform:
            return LINUX
        raise RuntimeError(
            "Unsupported platform detected: {}".format(sys.platform))

    def detect_devices(self):
        """Detect devices using either the Windows or Linux backend"""
        devices = get_device_list(VENDORS)
        for device in devices.copy():
            backend = self.get_backend(device)
            if backend is None:
                devices.remove(device)
                continue
            _, product = device
            if not backend.is_product_supported(product):
                devices.remove(device)
        return devices

    def get_backend(self, device):
        """Return the proper backend Keyboard class for a given device"""
        if device.vendor not in BACKENDS[self.platform]:
            return None
        module = BACKENDS[self.platform][device.vendor]
        try:
            exec("from {} import Keyboard".format(module))
        except ImportError as e:
            raise RuntimeError("Failed to load back-end {}".format(module))
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
