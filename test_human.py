#! /usr/bin/python3

import unittest
import os
import shutil
import pathlib
from human import Human, User, Admin
from custom_exceptions import (
    PasswordError,
    UserError,
    TwoPasswordError,
    RepUserError,
    ShortPasswordError,
)


class TestHuman(unittest.TestCase):
    """
    This test class is for testing Human Abstract class/
    methods and functionality
    """

    @classmethod
    def setUpClass(cls):
        cls.dirpath = "./test_database"
        cls.filepath = "./test_database/test.json"
        os.makedirs("./test_database")

    def test_json_create(self):
        """
        creating a file in test_database directory/
        and creating test.json to Testing json_create/
        static method in Human Abstract class
        """
        Human.json_create("./test_database/test.json")
        res = os.path.isfile("./test_database/test.json")
        self.assertEqual(res, True)

    def test_json_save_and_import(self):
        """
        Testing json_import and json_save static methods/
        functionality in Human Abstract class
        """
        dictionary = {"Matin": "Ghane"}
        Human.json_save(TestHuman.filepath, dictionary)
        res = Human.json_import(TestHuman.filepath)
        self.assertEqual(res, dictionary)

    def test_instantiating_abstract(self):
        """
        Instantiating an object from/
        Human abstract class Testing
        """
        with self.assertRaises(TypeError):
            Human("Matin", "Ghane", "bavaar", "matinghane", "1999/11/20")

    def test_hashing(self):
        """
        hashing static method Testing
        """
        res = "f3cce486ea320015c8e0ffae7cf"\
              "da6bc2c449a8980b1fb4c632703a70a998246"

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

    @classmethod
    def setUpClass(cls):
        cls.dirpath = pathlib.Path("./database")
        os.mkdir(TestUser.dirpath)
        cls.filepath = pathlib.Path("./database/users.json")
        Human.json_create(TestUser.filepath)

    def setUp(self):
        self.user1 = User(
            "Matin", "Ghane", "bavaar", "12345", "1999/11/20", "09197951537"
        )
        self.user2 = User(
            "Ali", "Alikhani", "aliii", "qwerty", "1997/10/03", "09121111111"
        )

    def test_get_obj(self):
        with self.assertRaises(UserError):
            User.get_obj("Ali", "qwerty")
        User.all_usernames.remove(self.user1.username)
        User.all_usernames.remove(self.user2.username)
        user2 = User.get_obj("bavaar", "12345")
        user3 = User.get_obj("aliii", "qwerty")
        test_dict = {user2.username: user2.__dict__,
                     user3.username: user3.__dict__}
        self.assertEqual(User.dictionary, test_dict)

    def test_sign_in_validation(self):
        with self.assertRaises(UserError):
            User.sign_in_validation("Ali", "123456")
        with self.assertRaises(PasswordError):
            User.sign_in_validation("bavaar", "matinghane")
        User.all_usernames.remove(self.user1.username)
        User.all_usernames.remove(self.user2.username)
        user2 = User.sign_in_validation("bavaar", "12345")
        user3 = User.sign_in_validation("aliii", "qwerty")
        test_dict = {user2.username: user2.__dict__,
                     user3.username: user3.__dict__}
        self.assertEqual(User.dictionary, test_dict)

    def test_signup(self):
        with self.assertRaises(RepUserError):
            User("Ali", "Alikhani", "bavaar", "12345",
                 "1999/10/18", "09365181897")
        with self.assertRaises(ShortPasswordError):
            User("mamad", "hosseini", "mamadi", "mam",
                 "1997/03/25", "09122222222")

    def test_edit_user(self):
        with self.assertRaises(RepUserError):
            self.user2.edit_user("bavaar")
        self.user1.edit_user("matin_ghane", "09365181897")
        self.user2.edit_user("", "09122222222")
        User.dictionary = Human.json_import(TestUser.filepath)
        self.assertEqual(
            User.dictionary[self.user1.username]["_username"], "matin_ghane"
        )
        self.assertEqual(
            User.dictionary[self.user1.username]["phone_number"], "09365181897"
        )
        self.assertEqual(
            User.dictionary[self.user2.username]["phone_number"], "09122222222"
        )

    def test_password_change(self):
        with self.assertRaises(PasswordError):
            self.user1.password_change("54321", "matinghane", "matinghane")
        with self.assertRaises(TwoPasswordError):
            self.user2.password_change("qwerty", "mrali", "mralii")
        with self.assertRaises(ShortPasswordError):
            self.user1.password_change("12345", "ma", "ma")
        self.user1.password_change("12345", "matinghane", "matinghane")
        User.dictionary = Human.json_import(TestUser.filepath)
        self.assertEqual(
            User.dictionary[self.user1.username]["_User__password"],
            Human.hashing("matinghane"),
        )

    def tearDown(self):
        User.all_usernames.clear()
        User.dictionary.clear()
        del self.user1
        del self.user2

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TestUser.dirpath)


class TestAdmin(unittest.TestCase):
    """
    This test class is for testing Admin class/
    methods and functionality
    """

    @classmethod
    def setUpClass(cls):
        cls.dirpath = pathlib.Path("./database")
        os.mkdir(TestAdmin.dirpath)
        cls.filepath = pathlib.Path("./database/admins.json")
        Human.json_create(TestAdmin.filepath)

    def setUp(self):
        self.admin1 = Admin("saman", "qwerty")
        self.admin2 = Admin("matin", "12345")

    def test_get_obj(self):
        with self.assertRaises(UserError):
            Admin.get_obj("Ali", "qwerty")
        Admin.all_usernames.remove(self.admin1.username)
        Admin.all_usernames.remove(self.admin2.username)
        admin2 = Admin.get_obj("matin", "12345")
        admin3 = Admin.get_obj("saman", "qwerty")
        test_dict = {admin2.username: admin2.__dict__,
                     admin3.username: admin3.__dict__}
        self.assertEqual(Admin.dictionary, test_dict)

    def test_sign_in_validation(self):
        with self.assertRaises(UserError):
            Admin.sign_in_validation("ali", "123456")
        with self.assertRaises(PasswordError):
            Admin.sign_in_validation("matin", "matinghane")
        Admin.all_usernames.remove(self.admin1.username)
        Admin.all_usernames.remove(self.admin2.username)
        admin2 = Admin.sign_in_validation("matin", "12345")
        admin3 = Admin.sign_in_validation("saman", "qwerty")
        test_dict = {admin2.username: admin2.__dict__,
                     admin3.username: admin3.__dict__}
        self.assertEqual(Admin.dictionary, test_dict)

    def test_signup(self):
        with self.assertRaises(RepUserError):
            Admin("matin", "matinghane")
        with self.assertRaises(ShortPasswordError):
            Admin("mamad", "mam")

    def test_edit_user(self):
        with self.assertRaises(RepUserError):
            self.admin2.edit_user("saman")
        self.admin1.edit_user("matin_ghane")
        Admin.dictionary = Human.json_import(TestAdmin.filepath)
        self.assertEqual(
            Admin.dictionary[self.admin1.username]["_username"], "matin_ghane"
        )

    def test_password_change(self):
        with self.assertRaises(PasswordError):
            self.admin1.password_change("ytrewq", "saman", "saman")
        with self.assertRaises(TwoPasswordError):
            self.admin2.password_change("12345", "matinghane", "matinghan")
        with self.assertRaises(ShortPasswordError):
            self.admin1.password_change("qwerty", "sa", "sa")
        self.admin1.password_change("qwerty", "saman", "saman")
        Admin.dictionary = Human.json_import(TestAdmin.filepath)
        self.assertEqual(
            Admin.dictionary[self.admin1.username]["_Admin__password"],
            Human.hashing("saman"),
        )

    def tearDown(self):
        Admin.all_usernames.clear()
        Admin.dictionary.clear()
        del self.admin1
        del self.admin2

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TestAdmin.dirpath)


def main():
    """
    This is our main module function
    """
    unittest.main()


if __name__ == "__main__":
    main()
