"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from pynput.keyboard import Key, KeyCode

alphanumeric = [
    '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
    'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'space', 'eu'
]
functionkeys = ["F{}".format(i) for i in range(1, 13)]
modifiers = [
    'capslock', 'enter', 'shift_l', 'shift_r', 'ctrl_l', 'win_l',
    'alt_l', 'alt_r', 'win_l', 'app', 'ctrl_r']
numpad = [
    'numlock', '(/)', '(*)', '(-)', '(7)', '(8)', '(9)', '(4)',
    '(5)', '(6)', '(+)', '(1)', '(2)', '(3)', '(enter)', '(0)',
    '(.)', '(00)'
]
controls = [
    'esc', 'printscreen', 'scrolllock', 'pause', 'backspace',
    'up', 'down', 'left', 'right', 'insert', 'home', 'pageup',
    'delete', 'end', 'pagedown', 'P1', 'P2', 'P3', 'P4'
]

pynput_rgb_keys = {
    Key.shift: "shift_l",
    Key.shift_l: "shift_l",
    Key.shift_r: "shift_r",
    Key.alt: "alt_l",
    Key.alt_gr: "alt_r",
    Key.alt_r: "alt_r",
    Key.alt_l: "alt_l",
    Key.backspace: "backspace",
    Key.pause: "pause",
    Key.esc: "esc",
    Key.print_screen: "printscreen",
    Key.scroll_lock: "scrollock",
    Key.up: "up",
    Key.down: "down",
    Key.left: "left",
    Key.right: "right",
    Key.insert: "insert",
    Key.home: "home",
    Key.page_up: "pageup",
    Key.delete: "delete",
    Key.end: "end",
    Key.page_down: "pagedown",
    Key.enter: "enter",
    Key.f1: "F1",
    Key.f2: "F2",
    Key.f3: "F3",
    Key.f4: "F4",
    Key.f5: "F5",
    Key.f6: "F6",
    Key.f7: "F7",
    Key.f8: "F8",
    Key.f9: "F9",
    Key.f10: "F10",
    Key.f11: "F11",
    Key.f12: "F12",
}

all = alphanumeric + functionkeys + modifiers + numpad + controls

pynput_rgb_keys.update({KeyCode(char=item): item for item in alphanumeric})

if __name__ == '__main__':
    print(len(alphanumeric) + len(functionkeys) + len(modifiers) + len(numpad) + len(controls))
