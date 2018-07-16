"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom
"""

if __name__ == '__main__':
    from .download import TARGETS
    import os

    DLL_FILES = list()
    DLL_DIR = os.path.dirname(os.path.realpath(__file__))

    for target in TARGETS.values():
        for file_name in target["files"].values():
            if os.path.exists(os.path.join(DLL_DIR, file_name)):
                continue
            DLL_FILES.append(target)
