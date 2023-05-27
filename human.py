#! /usr/bin/python3

from abc import ABC, abstractmethod
import datetime
import uuid
import hashlib
import json
from custom_exceptions import (
    UserError,
    RepUserError,
    ShortPasswordError,
    PasswordError,
    TwoPasswordError
)


class Human(ABC):
    """
    This is an Abstract class for Users and/
    Admin
    """
    def __init__(self, fname: str, lname: str,
                 username: str, password: str,
                 birth_date: str, phone_number: str = None,
                 user_id: str = None):
        self.fname, self.lname = fname, lname
        self.username, self.password = username, password
        if user_id is None:
            self.user_id = Human.uuid_gen()
        else:
            self.user_id = user_id
        self.phone_number = phone_number
        self.birth_date = birth_date

    @staticmethod
    def hashing(password: str):
        """
        This method is for hashing passwords
        """
        hashed_pass = (hashlib.sha256(password.encode("utf-8")).hexdigest())
        return hashed_pass

    @staticmethod
    def json_create(filename):
        """
        This method creates a json file when there/
        is no json file as a database to start the program.
        """
        with open(filename, mode="w+", encoding="utf-8") as f_1:
            json.dump({}, f_1)

    @staticmethod
    def json_save(filename, dictionary):
        """
        This static method save or dump our class dictionary into/
        database.json JSON fileeverytime use this method,/
        the JSON file emptied and rewrite the class dictionary into it
        """
        with open(filename, mode="w+", encoding="utf-8") as f_1:
            json.dump(dictionary, f_1, indent=4)

    @staticmethod
    def json_import(filename) -> dict:
        """
        This class method import whole content of database.json file into/
        our class dictionary with json.load() method
        """
        with open(filename, mode="r", encoding="utf-8") as f_1:
            return json.load(f_1)

    @classmethod
    @abstractmethod
    def get_obj(cls, username: str, password: str):
        """
        everytime we need to create an object in our class,/
        and take data from our imported dictionary from/
        database.json, such as login a user in out panel,/
        we use this method. we give it the/username and/
        password of the user and it will return an object/
        for us
        """
        pass

    def __str__(self):
        """
        This is a __str__ magic method for/
        returning user Information as a string
        """
        return f"\nUser Information:\n\tUsername: {self.username}\n\tPhone Number: {self.phone_number}\n\tUser ID: {self.user_id}"

    @classmethod
    @abstractmethod
    def sign_in_validation(cls, user_name: str, password: str):
        """
        This method is for sign in validation/
        and give username and password/
        if given username not in usernames list/
        rasing an Error that says Username not found
        and if entered username and password is/
        match to self.username and self.password
        printing sign in complete,/
        else if entered password is not match/
        print wrong password error.
        """
        pass

    @classmethod
    @abstractmethod
    def signup(cls, user_name: str, password: str, ph_numb: str = None):
        """
        This function is for Signing up users.
        first user must enter username, then enter password
        and finally enter phone number
        """
        pass

    @staticmethod
    def username_check(user_name: str):
        """
        This static method actually for checking repetitious usernames
        """
        if user_name in User.all_usernames:
            return False
        return True

    @abstractmethod
    def edit_user(self, usr_name: str, ph_numb: str = None):
        """
        This method is used for username and/
        phone number editing
        if given username or phone number in not None/
        , assigning given username and phone number/
        to this instance Attributes
        """
        pass

    @abstractmethod
    def password_change(self, old_pass: str, new_pass: str, rep_new_pass: str):
        """
        This function is for password changing.
        if entered old password in not match to original password/
        or new password and Repeat it not match together/
        raise an error.
        """

    @property
    @abstractmethod
    def username(self):
        """
        Getter for Username
        """
        pass

    @username.setter
    @abstractmethod
    def username(self, user_value):
        if not Human.username_check(user_value):
            raise RepUserError("Username is already taken! ")
        self._username = user_value

    @staticmethod
    def password_check(password: str) -> bool:
        """
        This function actually check the password and if its length smaller
        than 4, an ValueError raised with the too short massage
        """
        if len(password) < 4:
            return False
        return True

    @property
    @abstractmethod
    def password(self):
        """
        Getter for password
        """
        pass

    @password.setter
    @abstractmethod
    def password(self, password_value):
        pass

    @staticmethod
    def uuid_gen():
        """
        This function generate a universal unique identifier with uuid5
        and use MD5 Hash algorithm
        """
        return str(uuid.uuid4())


class User(Human):
    """
    This class is use for modeling users and some functionality/
    like username, password, a unique identifier and phone number./
    this class recieves informations from user and processing them./
    password must longer than 4 characters/
    username must be unique and repetitious usernames not accepted/
    also user can enter his/her phone number and if phone number not entered,
     it assuming to None
    """
    @staticmethod
    def hashing(password: str) -> str:
        """
        this is a static method that generates hash from a password
        and unique salt for each user
        """
        hashed_pass = (hashlib.sha256(password.encode("utf-8")).hexdigest())
        return hashed_pass

    all_usernames = []

    def __init__(
            self, fname: str, lname: str,
            username: str, password: str,
            birth_date: str, phone_number: str = None,
            user_id: str = None
            ):
        """
        The __init__ method for assigning attributes
        """
        super().__init__(fname, lname, username, password,
                         birth_date, phone_number, user_id)
        self.current_plan = "Bronze"
        self.wallet = 0
        User.all_usernames.append(self.username)
        if self.username not in User.dictionary:
            User.dictionary.update({self.username: self.__dict__})
            Human.json_save("users.json", User.dictionary)

    @classmethod
    def get_obj(cls, username, password):
        """
        everytime we need to create an object in our class,/
        and take data from our imported dictionary from/
        database.json, such as login a user in out panel,/
        we use this method. we give it the/username and/
        password of the user and it will return an object/
        for us
        """
        if username not in cls.dictionary:
            raise UserError("Username not found! ")
        for i, j in cls.dictionary.items():
            if i == username:
                return cls(
                        j["fname"],
                        j["lname"],
                        j["_username"],
                        password,
                        j["birth_date"],
                        j["join_date"],
                        j["phone_number"],
                        j["user_id"]
                        )

    def __str__(self):
        """
        This is a __str__ magic method for/
        returning user Information as a string
        """
        return f"\nUser Information:\n\tUsername: {self.username}\n\tPhone Number: {self.phone_number}\n\tUser ID: {self.user_id}"

    @classmethod
    def sign_in_validation(cls, user_name: str, password: str):
        """
        This method is for sign in validation/
        and give username and password/
        if given username not in usernames list/
        rasing an Error that says Username not found
        and if entered username and password is/
        match to self.username and self.password
        printing sign in complete,/
        else if entered password is not match/
        print wrong password error.
        """
        if user_name not in cls.dictionary:
            raise UserError("Username not found! ")
        new_key = Human.hashing(password)
        if cls.dictionary[user_name]["_User__password"] != new_key:
            raise PasswordError("Wrong Password!")
        usr_obj = cls.get_obj(user_name, password)
        return usr_obj

    dictionary = {}

    @classmethod
    def signup(cls, first_name: str, last_name: str,
               user_name: str, password: str,
               birth_date: str, ph_numb: str = None):
        """
        This function is for Signing up users.
        first user must enter username, then enter password
        and finally enter phone number
        """
        obj = cls(first_name, last_name,
                  user_name, password,
                  birth_date, ph_numb)
        return obj

    @staticmethod
    def username_check(user_name: str) -> bool:
        """
        This static method actually for checking repetitious usernames
        """
        if user_name in User.all_usernames:
            return False
        return True

    def edit_user(self, usr_name: str = None, ph_numb: str = None):
        """
        This method is used for username and/
        phone number editing
        if given username or phone number in not None/
        , assigning given username and phone number/
        to this instance Attributes
        """
        if usr_name in User.dictionary:
            raise RepUserError("Username already Taken! ")
        if usr_name != "":
            del User.dictionary[self.username]
            self.username = usr_name
            User.dictionary.update({self.username: self.__dict__})
            User.json_save("users.json", User.dictionary)
        if ph_numb != "":
            self.phone_number = ph_numb
            User.dictionary[self.username]["phone_number"] = ph_numb
            User.json_save("users.json", User.dictionary)

    def passwd_change(self, old_pass: str, new_pass: str, rep_new_pass: str):
        """
        This function is for password changing.
        if entered old password in not match to original password/
        or new password and Repeat it not match together/
        raise an error.
        """
        old_key = Human.hashing(old_pass)
        if old_key != self.password:
            raise PasswordError("Wrong original Password! ")
        if new_pass != rep_new_pass:
            raise TwoPasswordError("Unmatched new passwords")
        self.password = new_pass
        User.dictionary[self.username]["_User__password"] = self.password
        User.json_save("users.josn", User.dictionary)

    @property
    def username(self):
        """
        Getter for Username
        """
        return self._username

    @username.setter
    def username(self, user_value):
        if not Human.username_check(user_value):
            raise RepUserError("Username is already taken! ")
        self._username = user_value

    @staticmethod
    def password_check(password: str) -> bool:
        """
        This function actually check the password and if its length smaller
        than 4, an ValueError raised with the too short massage
        """
        if len(password) < 4:
            return False
        return True

    @property
    def password(self):
        """
        Getter for password
        """
        return self.__password

    @password.setter
    def password(self, passwd_value):
        if not Human.password_check(passwd_value):
            raise ShortPasswordError("Too short Password! ")
        key_value = Human.hashing(passwd_value)
        self.__password = key_value

    @staticmethod
    def uuid_gen():
        """
        This function generate a universal unique identifier with uuid5
        and use MD5 Hash algorithm
        """
        return str(uuid.uuid4())


class Admin(Human):
    """
    This class is for modeling Admins and/
    inherites from Human Abstract user.
    """
    all_usernames = []
    def __init__(self, username, password, user_id: str = None):
        self.username, self.password = username, password
        if user_id is None:
            self.user_id = Human.uuid_gen()
        else:
            self.user_id = user_id
        Admin.all_usernames.append(self.username)
        if self.username not in Admin.dictionary:
            Admin.dictionary.update({self.username: self.__dict__})
            User.json_save("admins.json", Admin.dictionary)

    @classmethod
    def get_obj(cls, username: str, password: str):
        """
        everytime we need to create an object in our class,/
        and take data from our imported dictionary from/
        database.json, such as login a user in out panel,/
        we use this method. we give it the/username and/
        password of the user and it will return an object/
        for us
        """
        if username not in cls.dictionary:
            raise UserError("Username not found! ")
        for i, j in cls.dictionary.items():
            if i == username:
                return cls(j["_username"], password)

    def __str__(self):
        """
        This is a __str__ magic method for/
        returning user Information as a string
        """
        return f"\nUser Information:\n\tUsername: {self.username}\n\tPhone Number: {self.phone_number}\n\tUser ID: {self.user_id}"

    @classmethod
    def sign_in_validation(cls, user_name: str, password: str):
        """
        This method is for sign in validation/
        and give username and password/
        if given username not in usernames list/
        rasing an Error that says Username not found
        and if entered username and password is/
        match to self.username and self.password
        printing sign in complete,/
        else if entered password is not match/
        print wrong password error.
        """
        if user_name not in cls.dictionary:
            raise UserError("Username not found! ")
        new_key = Human.hashing(password)
        if cls.dictionary[user_name]["_Admin__password"] != new_key:
            raise PasswordError("Wrong Password!")
        adm_obj = cls.get_obj(user_name, password)
        return adm_obj

    dictionary = {}

    @classmethod
    def signup(cls, user_name: str, password: str, ph_numb: str = None):
        """
        This function is for Signing up users.
        first user must enter username, then enter password
        and finally enter phone number
        """
        obj = cls(user_name, password)
        return obj

    def edit_user(self, usr_name: str, ph_numb: str = None):
        """
        This method is used for username and/
        phone number editing
        if given username or phone number in not None/
        , assigning given username and phone number/
        to this instance Attributes
        """
        if usr_name in Admin.dictionary:
            raise RepUserError("Username already Taken! ")
        if usr_name != "":
            del Admin.dictionary[self.username]
            self.username = usr_name
            Admin.dictionary.update({self.username: self.__dict__})
            Human.json_save("admins.json", User.dictionary)

    def passwd_change(self, old_pass: str, new_pass: str, rep_new_pass: str):
        """
        This function is for password changing.
        if entered old password in not match to original password/
        or new password and Repeat it not match together/
        raise an error.
        """
        old_key = Human.hashing(old_pass)
        if old_key != self.password:
            raise PasswordError("Wrong original Password! ")
        if new_pass != rep_new_pass:
            raise TwoPasswordError("Unmatched new passwords")
        self.password = new_pass
        User.dictionary[self.username]["_User__password"] = self.password
        User.json_save("users.josn", User.dictionary)

    @staticmethod
    def username_check(user_name: str) -> bool:
        """
        This static method actually for checking repetitious usernames
        """
        if user_name in User.all_usernames:
            return False
        return True

    @property
    def username(self):
        """
        Getter for Username
        """
        return self._username

    @username.setter
    def username(self, user_value):
        if not Human.username_check(user_value):
            raise RepUserError("Username is already taken! ")
        self._username = user_value

    @staticmethod
    def password_check(password: str) -> bool:
        """
        This function actually check the password and if its length smaller
        than 4, an ValueError raised with the too short massage
        """
        if len(password) < 4:
            return False
        return True

    @property
    def password(self):
        """
        Getter for password
        """
        return self.__password

    @password.setter
    def password(self, passwd_value):
        if not Human.password_check(passwd_value):
            raise ShortPasswordError("Too short Password! ")
        key_value = Human.hashing(passwd_value)
        self.__password = key_value

    @staticmethod
    def uuid_gen():
        """
        This function generate a universal unique identifier with uuid5
        and use MD5 Hash algorithm
        """
        return str(uuid.uuid4())


def main():
    """
    This is main function of our module
    """


if __name__ == "__main__":
    main()
