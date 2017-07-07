# Python RGB Keyboards Library
[![GPL License](https://img.shields.io/badge/license-GPL-blue.svg)](https://opensource.org/licenses/GPL-3.0)

This is a project that aims to create a universal RGB keyboard control library in Python. Using the varous SDKs
available and by creating wrappers around them, this library allows you to control the RGB keyboards of multiple
brands in a universal manner with the same function structure and arguments passed.

## Dependencies

### Packages
- `pynput`, available on PyPI
- `cue_sdk`, available on PyPI
- `pywinusb`, available on PyPI

### SDKs
For more information on how to retrieve the SDKs and install them to the right folder, please consult the `README.md`
file in the `sdks` folder.

## Keyboards
Though not all keyboards can be tested due to the fact that I only have a single mechanical RGB keyboard at my disposal 
to test the functions of the library, I have tried to integrate support for the following keyboards:

- Cooler Master
  * MasterKeys Pro L RGB (tested)
  * MasterKeys Pro M RGB
  * MasterKeys Pro S RGB
- Corsair
  * Gaming K65 RGB
  * Gaming K70 RGB
  * Gaming K95 RGB
  * Gaming Strafe RGB
- Logitech
  * Orion Spark G810
  * Orion Spark G910

Unfortunately, support for Razer keyboards is not available at this time. If you would like support for a keyboard, 
either request support for it on the issues page or fork the repository so you can write a wrapper around the SDK or
other type of functions yourself.

## License

        Python RGB Keyboards
        Copyright (C) 2017 RedFantom

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
## Goals
The goal of this project is to provide a universal interface for all RGB Keyboards for Python programmers with a
consistent function structure. I would like to include as many keyboards in the library as possible, but I can only
test the code for the Cooler MasterKeys SDK. If you experience any issues, please report them in the issues section.
Also, I'm planning to add universal effects to the repository using a wrapper around the classes, and providing
automatic detection of the keyboard connected.

## Contribute
If you would like to contribute to the project, by either reporting issues or writing code, that would be great! You can
either fork the repository, or you can send me an e-mail on [redfantom@outlook.com](mailto:redfantom@outlook.com) so I
can add you as a contributer to the project.

## Credits

- 10se1ucgo and JiFish for creating the [cue_sdk](https://github.com/10se1ucgo/cue_sdk) Python wrapper which is used in 
this project (Apache 2.0 License)
- Logitech for providing [logiPy](https://github.com/Logitech/logiPy) on GitHub (MIT License)

