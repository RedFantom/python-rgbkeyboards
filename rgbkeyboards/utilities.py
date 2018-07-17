"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from collections import namedtuple
import os
import sys


WINDOWS = "windows"
LINUX = "linux"

Device = namedtuple("Device", ["vendor", "product"])


def get_dll_path(path):
    """Return an absolute path to the SDK file specified"""
    if os.path.exists(path):
        return path
    path = os.path.join(get_sdks_path(), path)
    if not os.path.exists(path):
        raise RuntimeError("{} SDK DLL file missing".format(path))
    return path


def get_sdks_path():
    """Return an absolute path to the /sdks directory"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "sdks")


def get_platform():
    """Return a valid platform string"""
    if "win" in sys.platform:
        return WINDOWS
    elif "linux" in sys.platform:
        return LINUX
    raise RuntimeError("Unsupported platform: {}".format(sys.platform))


def get_device_list(vendors):
    """Return a list of Devices with a specific list of vendors"""
    device_list = list()

    def process(vendor, product):
        supported_vendor = vendor in vendors
        if not supported_vendor or vendor is None:
            return
        device = Device(vendor, product)
        if device in device_list:
            return
        device_list.append(device)

    if get_platform() is WINDOWS:
        from pywinusb import hid
        devices = hid.HidDeviceFilter().get_devices()
        for device in devices:
            if not isinstance(device, hid.HidDevice):
                continue
            vendor, product = device.vendor_name, device.product_name
            process(vendor, product)

    elif get_platform() is LINUX:
        import usb.core
        devices = usb.core.find(find_all=True)
        for device in devices:
            try:
                vendor, product = device.manufacturer, device.product
            except ValueError:
                continue
            process(vendor, product)

    return device_list
