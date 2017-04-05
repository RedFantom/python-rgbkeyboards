# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from corsair.corsair import Corsair
from masterkeys.masterkeys import MasterKeys
from logitech.logitech import Logitech
from pywinusb import hid


class Keyboards(object):
    BRANDS = ["Cooler Master", "Logitech", "Corsair"]
    MODELS = ["MasterKeys Pro L", "MasterKeys Pro M", "MasterKeys Pro S",
              "K65", "K70", "K95", "Strafe",
              "G810", "G910"]

    def __init__(self):
        pass

    def __exit__(self):
        pass

    def get_keyboard_manufacturer(self):
        all_devices = hid.HidDeviceFilter().get_devices_by_parent()
        manufacturers = []
        for parent, hid_items in all_devices.items():
            for item in hid_items:
                manufacturers.append(item.vendor_name)
        for brand in self.BRANDS:
            for manufacturer in manufacturers:
                if brand in manufacturer:
                    return brand
        raise ValueError("Product manufacturer could not be established.")

    def get_keyboard_model(self):
        all_devices = hid.HidDeviceFilter().get_devices_by_parent()
        products = []
        for parent, hid_items in all_devices.items():
            for item in hid_items:
                products.append(item.product_name)
        for model in self.MODELS:
            for product in products:
                if product in model:
                    return model
        raise ValueError("Product model could not be established.")

    def get_control_object(self):
        pass

    def get_setup_control_object(self):
        pass


if __name__ == '__main__':
    print Keyboards().get_keyboard_manufacturer()
    print Keyboards().get_keyboard_model()
