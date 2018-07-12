# Keyboard Back-ends
Each keyboard manufacturer uses a different interface with a different
SDK, and thus each keyboard brand requires a different back-end to allow
the library to control the keyboard. The back-ends offer a universal 
interface, optionally implementing brand-specific functionality, to
allow users to use the lighting on the keyboard in the same manner
across all keybaord brands and layouts.

## Back-ends

### Windows
Each of the Windows back-ends requires DLL-files from the SDK provided
by the manufacturer of the keyboard. See the README file in the `sdks`
folder in the package for more details.
- `masterkeys`, Cooler Master MasterKeys keyboard back-end
- `corsair`, Corsair keyboard back-end based on CUESDK
- `logitech`, Logitech back-end, depends on Logitech Gaming Software

### Linux
The Linux back-ends do not depend on files provided by the manufacturer,
as none of the manufacturers provide SDK files for Linux.
- [`masterkeys`](https://github.com/RedFantom/masterkeys-linux), 
  Python MasterKeys module, built upon `libmk`
  
## Interface
Each of the interfaces provides a single unified interface. To ensure 
the lowest possible latency, back-ends should not perform type checks
on arguments.

```python
class Keyboard:
    """
    Class supporting a single keyboard brand
    
    Note that effects are not supported by the universal interface as 
    each brand may have different effects or some effects may be 
    missing. Library functions such as initialization and control device
    selection should all be implemented in other ways. The first 
    supported keyboard found should always be chosen as the controlled
    device (currently only one keyboard per machine is supported).
    
    Functions should only if not raising an error would hide something 
    the user can influence from the user (like not having permission to 
    access the device). Otherwise, the function results should indicate
    success or failure.
    """
    
    def __init__(self, path):
        """
        :param path: Valid path to the DLL file if required. The DLL
            file location should be specified in `keyboards.py:PATHS`.
            If not required, should be omitted.
        """
        self._control = False
        
    def get_device_available(self)->bool:
        """Return availability of any device supported by this back-end"""
        
    def enable_control(self)->bool:
        """Enable the control of the first supported keyboard available"""
    
    def disable_control(self)->bool:
        """Disable the control on the controlled keyboard"""
        
    def set_full_led_color(self, r: int, g: int, b: int)->bool:
        """Set the color of the whole keyboard to a single color tuple"""
        
    def set_ind_led_color(self, leds: dict)->bool:
        """
        Set the color of all individual LEDs based on a dictionary
        
        The dictionary should have keynames, as defined in the 
        `keygroups.py` file as keys and int color tuples as values.
        All keys not in the dictionary should remain the color they
        had been set to previously (unless the keyboard changes modes).
        """
    
    @staticmethod
    def is_product_supported(iProduct):
        """
        Determine whether a product is supported by this back-end
        :param iProduct: USB descriptor iProduct string
        """
```

## Custom back-ends
Back-ends can be loaded into the module by manipulating the `BACKENDS`
dictionary in the `/keyboards.py` file. The dictionary is set up as 
follows:
```python
platform_name: {
    full_usb_manufacturer_string: 
        full_python_module_import_name
}
```

If the back-end depends on an SDK or DLL file that has to be passed to
the `__init__` function, the path should be specified in the `PATHS`
dictionary in the `/keyboards.py` file.

Both of these dictionaries are available through the `__init__.py` file
for easier access to the backends.
