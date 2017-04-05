# Python RGB Keyboards Library
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
    MIT License
    
    Copyright (c) 2017 RedFantom
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    
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

