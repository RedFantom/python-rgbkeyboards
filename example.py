"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from rgbkeyboards import Keyboards
from time import sleep


if __name__ == '__main__':
    kb = Keyboards().keyboard
    if kb is None:
        print("No valid back-end")
        exit()
    kb.enable_control()
    kb.set_full_led_color(255, 0, 0)
    sleep(1)
    kb.disable_control()
