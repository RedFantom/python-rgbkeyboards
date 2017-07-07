import os


def get_dll_path(name):
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, "sdks", name)
