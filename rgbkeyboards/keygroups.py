# Python RGB Keyboards, Copyright (C) 2017 by RedFantom
# All additions are under the copyright of their respective authors
# For license see LICENSE

alphanumeric = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
                'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
                'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
                'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
                'space', 'eu']
functionkeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
modifiers = ['capslock', 'enter', 'lshift', 'rshift', 'lctrl', 'lwin', 'lalt', 'ralt', 'lwin', 'app', 'rctrl']
keypad = ['numlock', '(/)', '(*)', '(-)', '(7)', '(8)', '(9)', '(4)', '(5)', '(6)', '(+)', '(1)', '(2)', '(3)',
          '(enter)', '(0)', '(.)', '(00)']
controls = ['esc', 'printscreen', 'scrolllock', 'pause', 'backspace', 'up', 'down', 'left', 'right', 'insert', 'home',
            'pageup', 'delete', 'end', 'pagedown', 'P1', 'P2', 'P3', 'P4']

if __name__ == '__main__':
    print(len(alphanumeric) + len(functionkeys) + len(modifiers) + len(keypad) + len(controls))
