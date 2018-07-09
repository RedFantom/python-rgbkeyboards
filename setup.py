"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from setuptools import setup

setup(
    name="rgbkeyboards",
    packages=["rgbkeyboards"],
    version="0.2.1",
    description="A library to control RGB Keyboards on Windows",
    author="RedFantom",
    url="https://www.github.com/RedFantom/python-rgb-keyboards",
    download_url="https://www.github.com/RedFantom/python-rgb-keyboards/releases",
    keywords=["RGB", "keyboard", "library"],
    license="MIT",
    classifiers=["Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: Microsoft :: Windows"],
    include_package_data=True,
    install_requires=["pywinusb", "cue_sdk", "pynput"],
    zip_safe=False
)
