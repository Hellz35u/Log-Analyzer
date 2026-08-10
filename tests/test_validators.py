import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import add_import_paths

add_import_paths()

from services.validators import validate_password, validate_username


class ValidateUsernameTests(unittest.TestCase):
    def test_valid_username(self):
        self.assertTrue(validate_username("bob"))

    def test_min_length_boundary(self):
        self.assertTrue(validate_username("abc"))

    def test_max_length_boundary(self):
        self.assertTrue(validate_username("1234567890"))

    def test_too_short(self):
        self.assertFalse(validate_username("ab"))

    def test_too_long(self):
        self.assertFalse(validate_username("12345678901"))

    def test_contains_space(self):
        self.assertFalse(validate_username("bo b"))

    def test_empty_string(self):
        self.assertFalse(validate_username(""))


class ValidatePasswordTests(unittest.TestCase):
    def test_valid_password(self):
        self.assertTrue(validate_password("password"))

    def test_min_length_boundary(self):
        self.assertTrue(validate_password("12345678"))

    def test_max_length_boundary(self):
        self.assertTrue(validate_password("1234567890123456"))

    def test_too_short(self):
        self.assertFalse(validate_password("1234567"))

    def test_too_long(self):
        self.assertFalse(validate_password("12345678901234567"))

    def test_contains_space(self):
        self.assertFalse(validate_password("pass word"))

    def test_empty_string(self):
        self.assertFalse(validate_password(""))


if __name__ == "__main__":
    unittest.main()
