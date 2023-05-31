#! /usr/bin/python3

import sys
import datetime
import argparse
from getpass import getpass
import os, platform
from movie import Film
from custom_exceptions import (
    UserError,
    RepUserError,
    PasswordError,
    TwoPasswordError,
    ShortPasswordError,
    FilmError,
    PhoneNumberError,
    AddTicketFailed,
    AlreadyExistAccount,
    FilmError,
    AddTicketFailed,
    TicketError,
    UnsuccessfulIdDeposit,
    UnsuccessfulAccountDeposit,
    UnsuccessfulPasswordDeposit,
    UnsuccessfulCvv2Deposit,
    BalanceMinimum
)
from human import Human, User, Admin


if platform.system() == "Linux":
    CLEAR_CMD = "clear"
else:
    CLEAR_CMD = "cls"


if not os.path.isdir("./database"):
    os.mkdir("./database")
if os.path.exists("./database/admins.json"):
    Admin.dictionary = Human.json_import("./database/admins.json")
else:
    Human.json_save("./database/admins.json", {})

if not os.path.isdir("./database"):
    os.mkdir("./database")
if os.path.exists("./database/films.json"):
    Film.films = Film.load_films_from_json("./database/films.json")
else:
    Film.save_films_to_json("./database/films.json", {})


# Admin signup through a scripting command - Checked: OK
parser = argparse.ArgumentParser(
    description="Take Username and Password from CLI and Create an Admin with those Information."
)
parser.add_argument("-u", "--username", type=str, help="Username of New Admin")
parser.add_argument("-p", "--password", type=str, help="Password of New Admin")
args = parser.parse_args()
if (args.username is not None) and (args.password is not None):
    try:
        Admin.signup(args.username, args.password)
    except RepUserError:
        os.system(CLEAR_CMD)
        print("Username Already Taken! \n")
        sys.exit("Exiting the Admin Creating Interface...")
    else:
        os.system(CLEAR_CMD)
        print("Admin Created! \n")
        sys.exit("\n\nExiting the Admin Creating Interface...")


while 1:
    os.system(CLEAR_CMD)
    print("\n***** - Welcome to cinema Ticket - *****\n")
    stat = input(
        "Stat:\n1 - User mode\n2 - Admin mode\n0 - Exit\nEnter command number: "
    )
    os.system(CLEAR_CMD)

    if stat == "1":
        if os.path.exists("./database/users.json"):
            User.dictionary = Human.json_import("./database/users.json")
        else:
            Human.json_save("./database/users.json", {})

        while 1:
            print("\n******** - Welcome to user management panel - ********\n")
            print("Stat:\n1 - Sign Up\n2 - Sign In\n0 - Exit\n")
            stat = input("Enter Command: ")
            os.system(CLEAR_CMD)

            # User sign up - Checked: OK.
            if stat == "1":
                print("\n********** ^ Sign up form ^ **********\n")
                fname = input("Enter First Name: ")
                lname = input("Enter Last Name: ")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                birth_date = input("Enter Birth date (YYYY-MM-DD): ")
                phone_number = input("Enter Phone number (e.g. 09876543210) : ")
                os.system(CLEAR_CMD)
                try:
                    User.signup(
                        fname, lname, username, password, birth_date, phone_number
                    )
                except RepUserError:
                    os.system(CLEAR_CMD)
                    print("\nUsername Already Taken! ")
                except ShortPasswordError:
                    os.system(CLEAR_CMD)
                    print("\nToo Short Password! ")
                except PhoneNumberError:
                    os.system(CLEAR_CMD)
                    print("Invalid phone number (e.g. 09876543210).")
                else:
                    os.system(CLEAR_CMD)
                    print("\nSigning Up Completed! ")

            elif stat == "2":
                print("\n************** - Login form - **************\n")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                os.system(CLEAR_CMD)
                try:
                    user_object = User.sign_in_validation(username, password)
                except UserError:
                    os.system(CLEAR_CMD)
                    print("\nUsername not Found! ")
                    continue
                except PasswordError:
                    os.system(CLEAR_CMD)
                    print("\nWrong Password! ")
                    continue
                else:
                    os.system(CLEAR_CMD)
                    print("\nSigning In Completed! ")

                while 1:
                    print("\n************ - User Dashboard - ************\n")
                    print(
                        "State:\n1 - Show User Information\n2 - Edit user info\n3 - Show available Tickets\n4 - Reserve Ticket\n5 - Charge Wallet\n0 - Back to Main Menu: "
                    )
                    stat = input("Enter Command: ")
                    os.system(CLEAR_CMD)
                    if stat == "1":
                        print(user_object)
                        print("List of Bank Accounts: ")
                        for i, j in User.dictionary[user_object.username][
                            "bank_accounts"
                        ].items():
                            print(i)
                            for m, k in j.items():
                                print(f"\n\t{m}: {k}")

                    elif stat == "2":
                        while 1:
                            print("\n***** ^ Edit User mode ^ *****\n")
                            print(
                                "State:\n1 - Edit profile\n2 - Password Change\n3 - Show Current Plan\n4 - Change Plan\n5 - Bank Accounts\n6 - Back to Dashboard"
                            )
                            stat = input("Enter Command: ")
                            os.system(CLEAR_CMD)
                            if stat == "1":
                                print("\n***** ^ Edit Profile mode ^ *****\n")
                                print(
                                    "For Abort to editing any item, just leave it and press Enter."
                                )
                                new_fname = input("Enter New First Name: ")
                                new_lname = input("Enter New Last Name: ")
                                new_b_date = input(
                                    "Enter New Birth Date (YYYY-MM-DD): "
                                )
                                new_usr = input("Enter New Username: ")
                                new_ph_numb = input("New Phone Number: ")
                                os.system(CLEAR_CMD)
                                try:
                                    user_object.edit_user(
                                        new_fname,
                                        new_lname,
                                        new_usr,
                                        new_ph_numb,
                                        new_b_date,
                                    )
                                except RepUserError:
                                    print("\nUsername already Taken! ")
                                else:
                                    print("\nUser Information has been Updated! ")

                            elif stat == "2":
                                print("\n******** ^ Password Change ^ ********\n")
                                old_p = getpass("Old Password: ")
                                new_p = getpass("New Password: ")
                                re_new_p = getpass("New Password again: ")
                                os.system(CLEAR_CMD)
                                try:
                                    user_object.password_change(old_p, new_p, re_new_p)
                                except PasswordError:
                                    print("\nWrong Original Password! ")
                                except TwoPasswordError:
                                    print("\nTwo new passwords are not matched! ")
                                except ShortPasswordError:
                                    print("Two Short New Password! ")
                                else:
                                    print("\nYour Password has been changed! ")

                            elif stat == "3":
                                print("***** ^ Show Current Plan ^ *****")
                                os.system(CLEAR_CMD)

                            elif stat == "4":
                                print("***** ^ Change Plan ^ *****")
                                os.system(CLEAR_CMD)

                            elif stat == "6":
                                print("Exiting User Edit Panel...")
                                break

                            elif stat == "5":
                                while 1:
                                    print("***** ^ Bank Accounts ^ *****")
                                    print(
                                        "State:\n1 - Add a Bank Account\n2 - Edit Bank Accounts\n3 - Exit Bank Accounts panel\n"
                                    )
                                    stat = input("Enter Command: ")
                                    os.system(CLEAR_CMD)
                                    if stat == "1":
                                        print("***** ^ Add Bank Account ^ *****")
                                        national_id = input("Enter National ID: ")
                                        account_name = input("Enter Account Name: ")
                                        balance = int(input("Enter Account Balance: "))
                                        account_password = getpass(
                                            "Enter Bank Account Password: "
                                        )
                                        os.system(CLEAR_CMD)
                                        try:
                                            user_object.add_bank_account(
                                                national_id,
                                                account_name,
                                                user_object.fname,
                                                user_object.lname,
                                                balance,
                                                account_password,
                                            )
                                        except AlreadyExistAccount:
                                            print("Account Name Already Exists! ")
                                        else:
                                            User.json_save(
                                                User.jsonpath, User.dictionary
                                            )
                                            print("Bank Account Add Successfully! \n")
                                            for i, j in User.dictionary[
                                                user_object.username
                                            ]["bank_accounts"][account_name].items():
                                                print(f"{i}: {j}")

                                    elif stat == "2":
                                        while 1:
                                            print("***** ^ Edit Bank Accounts ^ *****")
                                            print(
                                                "State:\n - Deposit\n2 - Exit Edit Bank Account Panel"
                                            )
                                            stat = input("Enter Command: ")
                                            os.system(CLEAR_CMD)

                                            if stat == "1":
                                                print(
                                                    "\n***** ^ Deposit Form ^ *****\n"
                                                )
                                                national_id = input(
                                                    "Enter National Id: "
                                                )
                                                account_name = input(
                                                    "Enter Account Name: "
                                                )
                                                depos = int(
                                                    input(
                                                        "Enter Amount of deposition: "
                                                    )
                                                )
                                                account_password = getpass(
                                                    "Enter Account Password: "
                                                )
                                                cvv2 = int(
                                                    getpass("Enter Account CVV2")
                                                )
                                                user_object.charge_bank_account(
                                                    user_object.username,
                                                    national_id,
                                                    account_name,
                                                    account_password,
                                                    cvv2,
                                                    depos,
                                                )

                                            elif stat == "3":
                                                print(
                                                    "Exiting Edit Bank Accounts panel..."
                                                )
                                                break

                                    elif stat == "3":
                                        print("Exit Bank Accounts Panel...")
                                        break

                    elif stat == "3":
                        print("***** ^ Ticket Menu ^ *****")
                        for i, j in Film.films.items():
                            print(i)
                            for m, k in j["tickets"].items():
                                print(f"\n\t{m}: {k}")

                    elif stat == "4":
                        os.system(CLEAR_CMD)
                        print("***** ^ Reserve Ticket ^ *****")
                        film_name = input("Enter Film Name: ")
                        year, month, day = input("Enter scene date (YYYY-MM-DD): ").split("-")
                        scene_date = datetime.date(int(year), int(month), int(day)).isoformat()
                        hour, minute = input("Enter Scene time (HH:MM): ").split(":")
                        scene_time = datetime.time(hour=int(hour), minute=int(minute)).isoformat(timespec="minutes")
                        quantity = int(input("Enter Quantity: "))
                        print("\n***** ^ Checkout Form ^ *****\n")
                        national_id = input("Enter National ID: ")
                        account_name = input("enter Account Name: ")
                        password = getpass("Enter password: ")
                        cvv2 = int(input("Enter CVV2: "))
                        try:
                            User.reserve_ticket(film_name, scene_date, scene_time, quantity, national_id, account_name, password, cvv2)
                        except FilmError:
                            os.system(CLEAR_CMD)
                            print("Film Not Found! ")
                        except TicketError:
                            os.system(CLEAR_CMD)
                            print("ticket Not Found! ")
                        except UnsuccessfulIdDeposit:
                            os.system(CLEAR_CMD)
                            print("National Id Not Found! ")
                        except UnsuccessfulAccountDeposit:
                            os.system(CLEAR_CMD)
                            print("Account Not Found! ")
                        except UnsuccessfulPasswordDeposit:
                            os.system(CLEAR_CMD)
                            print("Wrong Password! ")
                        except UnsuccessfulCvv2Deposit:
                            os.system(CLEAR_CMD)
                            print("Wrong CVV2")
                        except BalanceMinimum:
                            os.system(CLEAR_CMD)
                            print("Minimum Balance Reached! ")
                        else:
                            os.system(CLEAR_CMD)
                            print("Ticket(s) Reserved Successfully! ")

                    elif stat == "5":
                        os.system(CLEAR_CMD)
                        print("***** ^ Wallet Charge Menu ^ *****")
                        national_id = input("Enter National ID: ")
                        account_name = input("Enter Account Name: ")
                        password = getpass("Enter Account Password: ")
                        cvv2 = int(input("Enter CVV2: "))
                        amount = int(input("Enter Amount: "))
                        try:
                            user_object.charge_wallet(national_id, account_name, password, cvv2, amount)
                        except UnsuccessfulIdDeposit:
                            os.system(CLEAR_CMD)
                            print("National Id Not Found! ")
                        except UnsuccessfulAccountDeposit:
                            os.system(CLEAR_CMD)
                            print("Account Not Found! ")
                        except UnsuccessfulPasswordDeposit:
                            os.system(CLEAR_CMD)
                            print("Wrong Password! ")
                        except UnsuccessfulCvv2Deposit:
                            os.system(CLEAR_CMD)
                            print("Wrong CVV2")
                        except BalanceMinimum:
                            os.system(CLEAR_CMD)
                            print("Minimum Balance Reached! ")
                        else:
                            os.system(CLEAR_CMD)
                            print("Your Wallet Charged successfully! ")

                    elif stat == "0":
                        print("\nExiting User Panel...")
                        user_object.delete_user()
                        break

                    else:
                        print("\nInvalid State! ")
                        continue

            # Exit command - Checked: OK.
            elif stat == "0":
                os.system(CLEAR_CMD)
                print("\nExiting the User Management Panel... ")
                break
            # Invalid State command - Checked: OK.
            else:
                os.system(CLEAR_CMD)
                print("\nInvalid State! ")
                continue

    elif stat == "2":
        while 1:
            print("\n******** - admin management panel - ********\n")
            stat = input("Stat:\n1 - Sign In\n0 - Exit\nEnter command number:  ")
            os.system(CLEAR_CMD)

            # Admin log in - Checked: OK.
            if stat == "1":
                print("\n************** - Login form - **************\n")
                try:
                    username = input("Enter Username: ")
                    password = getpass("Enter Password: ")
                    admin_object = Admin.sign_in_validation(username, password)
                except UserError:
                    os.system(CLEAR_CMD)
                    print("\nUsername not Found! ")
                    continue
                except PasswordError:
                    os.system(CLEAR_CMD)
                    print("\nWrong Password! ")
                    continue
                else:
                    os.system(CLEAR_CMD)
                    print("\nSigning In Completed! ")
                    if os.path.isfile("./database/films.json"):
                        Film.films = Film.load_films_from_json("./database/films.json")
                    else:
                        Film.save_films_to_json("./database/films.json", {})

                while 1:
                    print("\n************ - Admin Dashboard - ************\n")
                    stat = input(
                        "Stat:\n1 - Add film\n2 - Remove film\n3 - Add Ticket\n4 - Show Your Information\n5 - Edit Username\n6 - Password Change\n0 - Back to Main Menu\nEnter command number: "
                    )
                    os.system(CLEAR_CMD)
                    # Add new film - Checked: OK.
                    if stat == "1":
                        print("\n************** ^ Add film ^ **************\n")
                        film_name = input("Film name: ")
                        film_genre = input(
                            "Film genre (e.g. Comedy/Action/Romance e.t.): "
                        )
                        age_rate = input("Film age rating: ")
                        Admin.add_film(film_name, film_genre, age_rate)
                        os.system(CLEAR_CMD)
                        print("\nFilm added successfully! \n")

                    # Remove film - Checked: OK.
                    elif stat == "2":
                        print("********** ^ Remove Film ^ **********")
                        film_name = input("Enter Film Name to Remove: ")
                        try:
                            Admin.remove_film(film_name)
                        except FilmError:
                            os.system(CLEAR_CMD)
                            print("Film with this Name not found for Remove! ")
                            continue
                        else:
                            os.system(CLEAR_CMD)
                            print("Film Removed Successfully! ")

                    # Add ticket - Checked: OK.
                    elif stat == "3":
                        print("***** ^ Add Ticket ^ *****")
                        film_name = input("Enter Film Name: ")
                        year, month, day = input(
                            "Enter scene date (YYYY-MM-DD): "
                        ).split("-")
                        film_date = datetime.date(
                            int(year), int(month), int(day)
                        ).isoformat()
                        hour, minute = input("Enter Scene time (HH:MM): ").split(":")
                        scene_time = datetime.time(
                            hour=int(hour), minute=int(minute)
                        ).isoformat(timespec="minutes")
                        ticket_capacity = int(input("Enter the Scene Capacity: "))
                        ticket_price = int(input("Enter the Ticket Price: "))
                        try:
                            Admin.add_show(
                                film_name,
                                film_date,
                                scene_time,
                                ticket_capacity,
                                ticket_price,
                            )
                        except AddTicketFailed:
                            os.system(CLEAR_CMD)
                            print("Incorrect data, please check information.")
                        else:
                            os.system(CLEAR_CMD)
                            print("\nTicket Added Successfully! \n")

                    # Admin info - Checked: OK.
                    elif stat == "4":
                        os.system(CLEAR_CMD)
                        print(admin_object)

                    # Edit admin info - Checked: OK
                    elif stat == "5":
                        print("********** ^ admin Edit Username ^ **********")
                        print("To abort changes, leave it blank.\n")
                        new_username = input("Enter New Username: ")
                        new_ph_numb = input("Enter New Phone Number: ")
                        try:
                            admin_object.edit_user(new_username, new_ph_numb)
                        except RepUserError:
                            os.system(CLEAR_CMD)
                            print("\nUsername already Taken! ")
                        except PhoneNumberError:
                            os.system(CLEAR_CMD)
                            print("Invalid Phone Number format! ")
                        else:
                            os.system(CLEAR_CMD)
                            print("\nUser Information has been Updated! ")

                    # Change admin password - Checked: OK
                    elif stat == "6":
                        print("\n********** ^ Password Change ^ **********\n")
                        old_pass = getpass("Enter Old Password: ")
                        new_pass = getpass("Enter New Password: ")
                        rep_new_pass = getpass("Enter New Password again: ")
                        try:
                            admin_object.password_change(
                                old_pass, new_pass, rep_new_pass
                            )
                        except PasswordError:
                            os.system(CLEAR_CMD)
                            print("\nWrong Old Password! ")
                        except TwoPasswordError:
                            os.system(CLEAR_CMD)
                            print("\nTwo new passwords doesnt match! ")
                        except ShortPasswordError:
                            os.system(CLEAR_CMD)
                            print("New Password is too short! ")
                        else:
                            os.system(CLEAR_CMD)
                            print("\nYour Password has been changed! ")

                    # Exit command - Checked: OK
                    elif stat == "0":
                        os.system(CLEAR_CMD)
                        print("\nExiting Admin Panel...")
                        admin_object.delete_admin()
                        break
                    # Invalid state command - Checked: OK
                    else:
                        os.system(CLEAR_CMD)
                        print("\nInvalid State! ")
                        continue

            elif stat == "0":
                print("\nExiting the Admin Management Panel... ")
                break

            else:
                os.system(CLEAR_CMD)
                print("\nInvalid State! ")
                continue

    elif stat == "0":
        os.system(CLEAR_CMD)
        print("Exiting the program...")
        break

    else:
        os.system(CLEAR_CMD)
        print("Invalid stat.")
        continue
