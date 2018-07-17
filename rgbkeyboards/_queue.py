"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
import sys


def is_python_3():
    return sys.version_info[0] == 3


if is_python_3():
    from queue import *
else:
    from Queue import *
