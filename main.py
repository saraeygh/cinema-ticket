#! /usr/bin/python3

from os import path
from getpass import getpass
from users import (
        User,
        UserError,
        RepUserError,
        PasswordError,
        TwoPasswordError,
        ShortPasswordError
        )

if path.exists("./database.json"):
    User.json_import()
else:
    User.json_create()

while 1:
    print("\n********** - Welcome to user management panel - **********\n")
    User.dictionary = User.json_import()
    stat = input("Stat (0(Exit) - 1(Sign Up) - 2(Sign In)):   ")
    if stat == "5":
        print("***** ^ Secret Admin panel ^ *****")
        print(User.dictionary.keys(), end="\n\n")
        for i, j in User.dictionary.items():
            print(f"\n{i}")
            for m, n in j.items():
                print(f"\t{m}:\t{n}")

    elif stat == "1":
        print("\n********** ^ Sign up form ^ **********\n")
        try:
            username = input("Enter Username: ")
            password = getpass("Enter Password: ")
            phone_number = input("Enter Phone number(Optional): ")
            User.signup(username, password, phone_number)
        except RepUserError:
            print("\nUsername Already Taken! ")
        except ShortPasswordError:
            print("\nToo Short Password! ")
        else:
            print("\nSigning Up Completed! ")

    elif stat == "2":
        print("\n************** - Login form - **************\n")
        try:
            username = input("Enter Username: ")
            password = getpass("Enter Password: ")
            user_object = User.sign_in_validation(username, password)
        except UserError:
            print("\nUsername not Found! ")
            continue
        except PasswordError:
            print("\nWrong Password! ")
            continue
        else:
            print("\nSigning In Completed! ")

        while 1:
            print("\n************** - User Dashboard - **************\n")
            stat = input("Stat (1(Show User Information) - 2(Edit) - 3(Password Change) - 4(Back to Main Menu)):   ")

            if stat == "1":
                print(user_object)

            elif stat == "2":
                print("\n******** ^ Edit User information mode ^ ********\n")
                print("wouldn\'t change any item, leave it and press Enter.\n")
                try:
                    new_username = input("Enter New Username: ")
                    new_phone_number = input("Enter New Phone Number: ")
                    user_object.edit_user(new_username, new_phone_number)
                except RepUserError:
                    print("\nUsername already Taken! ")
                else:
                    print("\nUser Information has been Updated! ")

            elif stat == "3":
                print("\n********** ^ Password Change ^ **********\n")
                try:
                    old_pass = getpass("Enter Old Password: ")
                    new_pass = getpass("Enter New Password: ")
                    rep_new_pass = getpass("Enter New Password again: ")
                    user_object.passwd_change(old_pass, new_pass, rep_new_pass)
                except PasswordError:
                    print("\nWrong Original Password! ")
                except TwoPasswordError:
                    print("\nTwo new passwords are not matched! ")
                except ShortPasswordError:
                    print("Two Short New Password! ")
                else:
                    print("\nYour Password has been changed! ")

            elif stat == "4":
                del user_object
                print("\nExiting User Panel...")
                break

            else:
                print("\nInvalid State! ")
                continue

    elif stat == "0":
        print("\nExiting the User Management Panel... ")
        break

    else:
        print("\nInvalid State! ")
        continue
