"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from setuptools import setup, find_packages
from setuptools.command.install import install
from sys import platform

if "win" in platform:
    requirements = ["cue_sdk", "pywinusb"]
elif "linux" in platform:
    requirements = ["masterkeys", "pyusb"]
else:
    raise RuntimeError("Unsupported platform: {}".format(platform))


class CustomInstall(install):
    """Customized install to allow the user to download"""

    def run(self, *args):
        """Download the SDKs for the Windows back-ends if on Windows"""
        if "win" in platform:
            from rgbkeyboards.sdks.download import download_dlls
            download_dlls()
        install.run(self)


setup(
    name="rgbkeyboards",
    packages=find_packages(),
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
    install_requires=requirements + ["pynput"],
    zip_safe=False
)
