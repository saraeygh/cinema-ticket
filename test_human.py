#! /usr/bin/python3

import unittest
import os
import shutil
import pathlib
from human import Human, User, Admin
from custom_exceptions import (
        FileError, PasswordError,
        UserError, TwoPasswordError,
        RepUserError, ShortPasswordError
        )


class TestHuman(unittest.TestCase):
    """
    This test class is for testing Human Abstract class/
    methods and functionality
    """

    @classmethod
    def setUpClass(cls):
        os.makedirs("./test_database")

    def test_json_create(self):
        Human.json_create("./test_database/test.json")
        res = os.path.isfile("./test_database/test.json")
        self.assertEqual(res, True)

    def test_instantiating_abstract(self):
        """
        Instantiating an object from/
        Human abstract class Testing
        """
        with self.assertRaises(TypeError):
            human1 = Human("Matin", "Ghane", "bavaar",
                           "matinghane", "1999/11/20")

    def test_hashing(self):
        """
        hashing static method Testing
        """
        res = "f3cce486ea320015c8e0ffae7cfda6bc2c449a8980b1fb4c632703a70a998246"
        self.assertEqual(Human.hashing("matin"), res)

    def test_username_check(self):
        """
        username_check static method Testing
        """
        user_list = ["Matin", "John", "Ali", "Corey", "Mamad"]
        self.assertTrue(Human.username_check("Sara", user_list))
        self.assertFalse(Human.username_check("Ali", user_list))

    def test_password_check(self):
        """
        password_check static method Testing
        """
        self.assertTrue(Human.password_check("abcdef"))
        self.assertFalse(Human.password_check("ma"))

    @classmethod
    def tearDownClass(cls):
        mydir = pathlib.Path("./test_database")
        shutil.rmtree(mydir)


class TestUser(unittest.TestCase):
    """
    This test class is for testing User class/
    methods and functionality
    """
    pass


class TestAdmin(unittest.TestCase):
    """
    This test class is for testing Admin class/
    methods and functionality
    """
    pass


def main():
    """
    This is our main module function
    """
    unittest.main()


if __name__ == "__main__":
    main()
