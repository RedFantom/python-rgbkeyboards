"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from os import system, path
from setuptools import setup
from sys import platform, argv as args, executable

if "win" in platform:
    requirements = ["cue_sdk", "pywinusb"]
    if "install" in args:
        script = path.join(path.dirname(path.abspath(__file__)),
                           "rgbkeyboards", "sdks", "download.py")
        system("{} {}".format(executable, script))
elif "linux" in platform:
    requirements = ["masterkeys", "pyusb"]
else:
    raise RuntimeError("Unsupported platform: {}".format(platform))

setup(
    name="rgbkeyboards",
    packages=["rgbkeyboards"],
    package_data={"rgbkeyboards": ["sdks/*.dll"]},
    version="0.2.1",
    description="A library to control RGB Keyboards",
    author="RedFantom",
    url="https://github.com/RedFantom/python-rgb-keyboards",
    download_url="https://github.com/RedFantom/python-rgb-keyboards/releases",
    keywords=["RGB", "keyboard", "library"],
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)
