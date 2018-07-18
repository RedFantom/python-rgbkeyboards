"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from contextlib import contextmanager
from threading import Lock
from ._queue import Queue


class BaseKeyboard(object):
    """
    Defines the interface described in BACKENDS.md

    :attribute _control: Flag to be set to True when keyboard control is
        enabled. Should only be set after successfully enabling keyboard
        control, so only after error checking.

    Note that type checking on the arguments of all functions is done
    using assertions. This means that they are stripped out if
    Python is run with the -O flag, saving a little bit of execution
    time.
    """
    def __init__(self, *args):
        """Initialize attributes and properties"""
        self._lock = Lock()
        self._effect_queue = Queue()
        self._control = False
        # Back-end defined
        self._setup_lib(*args)

    def enable_control(self):
        """Enable control on the first found supported keyboard"""
        if self._control is True:
            return True
        if self.get_device_available() is False:
            return False
        r = self._exec_func(self._enable_control)
        if r is True:
            self._control = True
        return r

    def disable_control(self):
        """Disable control on the controlled keyboard"""
        if self._control is False:
            return True
        r = self._exec_func(self._disable_control)
        if r is True:
            self._control = False
        return r

    def set_full_color(self, r, g, b):
        """Set the keyboard of all the LEDs of the keyboard"""
        assert self._control, "Control is not enabled"
        assert all(isinstance(v, int) for v in (r, g, b)), \
            "Not all arguments are of int type"
        assert all(-1 < v < 256 for v in (r, g, b)), \
            "Not all arguments are in byte range"
        return self._exec_func(self._set_full_color, r, g, b)

    def set_ind_color(self, keys):
        """Set the color of all LEDs on the keyboard individually"""
        assert isinstance(keys, dict), "param keys is not a dictionary"
        assert all(isinstance(value, tuple) for value in keys.values()), \
            "keys dict does not contain only proper color tuples"
        assert all(isinstance(key, str) for key in keys.keys()), \
            "keys dict does not contain only str keys"
        assert self._control is True, "Control is not enabled"
        return self._exec_func(self._set_ind_color, keys)

    def get_device_available(self, *args):
        """Return whether a supported device is available"""
        return self._exec_func(self._get_device_available, *args)

    @contextmanager
    def control(self):
        """Context manager granting control on __enter__ and release"""
        if self.get_device_available() is False:
            raise ValueError("No device available")
        try:
            self.enable_control()
            yield
        finally:
            self.disable_control()

    @property
    def is_control_enabled(self):
        """Read only access to _control flag"""
        return self._control

    def _exec_func(self, func, *args):
        """Execute a function with the library in a thread-safe manner"""
        self._lock.acquire()
        r = func(*args)
        self._lock.release()
        return r

    """
    Abstract Functions: To be implemented by back-end
    
    Correct arguments to the functions, a loaded library and keyboard 
    control can be assumed in these functions. The have a private prefix
    and thus should not be called by users.
    """

    def _setup_lib(self, *args):
        """
        Load the library required for the back-end

        Importing additional modules, defining additional instance
        attributes: it should all happen here. Imports should be lazy
        to ensure compatibility and as this function is called in
        __init__ creating attributes in this function is allowed.
        """
        raise NotImplementedError()

    def _enable_control(self):
        """Enable control using the back-end library"""
        raise NotImplementedError()

    def _disable_control(self):
        """
        Release control using the back-end library
        :return: bool
        """
        raise NotImplementedError()

    def _set_ind_color(self, keys):
        """
        Set the color of individual keys on the keyboard

        Should not influence the color of any key colors already set if
        that is possible with the library. Otherwise, consider using a
        key color cache as an instance attribute.
        :param keys: Dictionary of {keyname: (r, g, b)
        :return: bool
        """
        raise NotImplementedError()

    def _set_full_color(self, r, g, b):
        """
        Set the color of all LEDs available on the keyboard

        May override all colors set using _set_ind_color, or even
        put the keyboard in an entirely different lighting mode. Should
        be optimized for a low-latency approach.
        :param r, g, b: RGB color tuple values
        :return: bool
        """
        raise NotImplementedError()

    def _get_device_available(self, *args):
        """
        Determine whether any supported device is available

        The back-end may override the get_device_available function if
        no actual non-thread-safe actions are performed when calling
        this function. Additional arguments can be implemented for
        use within the back-end.
        :return: bool
        """
        raise NotImplementedError()

    @staticmethod
    def is_product_supported(product):
        """Return whether a product is supported by iProduct USB string"""
        raise NotImplementedError()
