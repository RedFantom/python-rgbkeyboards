# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE
from corsair.corsair import Corsair
from masterkeys.masterkeys import MasterKeys
from logitech.logitech import Logitech
from pywinusb import hid
import cue_sdk


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
        """
        Get the name of the keyboard manufacturer by accessing the win32api
        :return: str such as in BRANDS
        """
        all_devices = hid.HidDeviceFilter().get_devices_by_parent()
        manufacturers = []
        for parent, hid_items in list(all_devices.items()):
            for item in hid_items:
                manufacturers.append(item.vendor_name)
        for brand in self.BRANDS:
            for manufacturer in manufacturers:
                if brand in manufacturer:
                    return brand
        raise ValueError("Product manufacturer could not be established.")

    def get_keyboard_model(self):
        """
        Get the name of the keyboard model by accessing the win32api
        :return: str such as in MODELS
        """
        all_devices = hid.HidDeviceFilter().get_devices_by_parent()
        products = []
        for parent, hid_items in list(all_devices.items()):
            for item in hid_items:
                products.append(item.product_name)
        for model in self.MODELS:
            for product in products:
                if product in model:
                    return model
        raise ValueError("Product model could not be established.")

    def get_control_object(self):
        """
        Get a control object for the user's keyboard automatically
        :return: object
        """
        manufacturer = self.get_keyboard_manufacturer()
        if manufacturer == "Cooler Master":
            return MasterKeys()
        elif manufacturer == "Logitech":
            return Logitech()
        elif manufacturer == "Corsair":
            return Corsair()
        else:
            raise ValueError("No valid manufacturer found.")

    def get_setup_control_object(self):
        """
        Get a control object that is fully setup and ready to use with its functions
        :return: object
        """
        manufacturer = self.get_keyboard_manufacturer()
        model = self.get_keyboard_model()
        if manufacturer == "Cooler Master":
            keyboard = MasterKeys()
            if model == "MasterKeys Pro L":
                keyboard.set_control_device(MasterKeys.RGB_L)
            elif model == "MasterKeys Pro M":
                keyboard.set_control_device(MasterKeys.RGB_M)
            elif model == "MasterKeys Pro S":
                keyboard.set_control_device(MasterKeys.RGB_S)
            else:
                raise ValueError("No valid manufacturer/model combination found.")
            keyboard.set_led_control_enabled(True)
            return keyboard
        elif manufacturer == "Logitech":
            keyboard = Logitech()
            if model == "G810":
                keyboard.set_control_device(Logitech.RGB_PK)
            elif model == "G910":
                keyboard.set_control_device(Logitech.RGB_ST)
            else:
                raise ValueError("No valid manufacturer/model combination found.")
        elif manufacturer == "Corsair":
            keyboard = Corsair()
            keyboard.set_control_device(cue_sdk.CDT.Keyboard)
            return keyboard
        else:
            raise ValueError("No valid manufacturer found.")


if __name__ == '__main__':
    print(Keyboards().get_keyboard_manufacturer())
    print(Keyboards().get_keyboard_model())
