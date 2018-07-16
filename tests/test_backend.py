"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from time import sleep
from unittest import TestCase
# Project Modules
from rgbkeyboards import BaseKeyboard, Keyboards


class TestKeyboards(TestCase):
    """Tests the Keyboards class and the backend provided by it"""

    def setUp(self):
        self.kb = Keyboards().keyboard
        if self.kb is None:
            raise RuntimeError("No keyboard connected")
        if not isinstance(self.kb, BaseKeyboard):
            raise RuntimeError("Backend not implemented properly")

    def test_backend_type(self):
        self.assertIsInstance(self.kb, BaseKeyboard)

    def test_enable_control(self):
        r = self.kb.enable_control()
        self.assertIsInstance(r, bool)
        self.assertTrue(r)

    def test_set_full_led_color(self):
        self.kb.enable_control()
        r = self.kb.set_full_led_color(255, 255, 0)
        self.assertIsInstance(r, bool)
        self.assertTrue(r)

    def test_set_ind_led_color(self):
        self.kb.enable_control()
        r = self.kb.set_ind_led_color({"esc": (0, 255, 0)})
        self.assertIsInstance(r, bool)
        self.assertTrue(r)

    def tearDown(self):
        if self.kb.is_control_enabled is True:
            self.kb.disable_control()
        sleep(1)

