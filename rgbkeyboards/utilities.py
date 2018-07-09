"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
import os


def get_dll_path(path):
    """Return an absolute path to the SDK file specified"""
    if os.path.exists(path):
        return path
    return os.path.join(get_sdks_path(), path)


def get_sdks_path():
    """Return an absolute path to the /sdks directory"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "sdks")
