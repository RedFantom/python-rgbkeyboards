"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from rgbkeyboards import Keyboards, keygroups
from time import sleep


if __name__ == '__main__':
    kb = Keyboards().keyboard
    keys = {key: (255, 255, 255) for key in keygroups.all}
    if kb is None:
        print("No valid back-end")
        exit()
    kb.enable_control()
    kb.set_ind_color(keys)
    sleep(1)
    kb.disable_control()
