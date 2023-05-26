#! /usr/bin/python3
from getpass import getpass
from users import (
        User,
        UserError,
        RepUserError,
        PasswordError,
        TwoPasswordError,
        ShortPasswordError
        )


while 1:
    print("\n********** - Welcome to user management panel - **********\n")
    try:
        stat = input("Stat (0(Exit) - 1(Sign Up) - 2(Sign In)):   ")
    except NameError:
        print("\nInvalid State! ")
        continue
    if stat == "5":
        print("***** ^ Secret Admin panel ^ *****")
        print(User.all_usernames, end="\n\n")
        for i in User.all_hashes:
            print(i)
        for i, j in User.dictionary.items():
            print(j, i, sep="\t")

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
            USER_OBJECT = User.sign_in_validation(username, password)
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
                USER_OBJECT.representation()

            elif stat == "2":
                print("\n******** ^ Edit User information mode ^ ********\n")
                print("if you dont want to change any item, leave it and press Enter.\n")
                try:
                    new_username = input("Enter New Username: ")
                    new_phone_number = input("Enter New Phone Number: ")
                    USER_OBJECT.edit_user(new_username, new_phone_number)
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
                    USER_OBJECT.passwd_change(old_pass, new_pass, rep_new_pass)
                except PasswordError:
                    print("\nWrong Original Password! ")
                except TwoPasswordError:
                    print("\nTwo new passwords are not matched! ")
                except ShortPasswordError:
                    print("Two Short New Password! ")
                else:
                    print("\nYour Password has been changed! ")

            elif stat == "4":
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
