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
    AddTicketFailed
)
from human import Human, User, Admin


if platform.system() == "Linux":
    clear_cmd = "clear"
else:
    clear_cmd = "cls"


if not os.path.isdir("./database"):
    os.mkdir("./database")
if os.path.exists("./database/admins.json"):
    Admin.dictionary = Human.json_import("./database/admins.json")
else:
    Human.json_save("./database/admins.json", {})

# Admin signup through a scripting command - Checked: OK
parser = argparse.ArgumentParser(description="Take Username and Password from CLI and Create an Admin with those Information.")
parser.add_argument("-u", "--username", type=str, help="Username of New Admin")
parser.add_argument("-p", "--password", type=str, help="Password of New Admin")
args = parser.parse_args()
if (args.username is not None) and (args.password is not None):
    try:
        Admin.signup(args.username, args.password)
    except RepUserError:
        os.system(clear_cmd)
        print("Username Already Taken! \n")
        sys.exit("Exiting the Admin Creating Interface...")
    else:
        os.system(clear_cmd)
        print("Admin Created! \n")
        sys.exit("\n\nExiting the Admin Creating Interface...")


while 1:
    print("\n***** - Welcome to cinema Ticket - *****\n")
    stat = input("Stat:\n1 - User mode\n2 - Admin mode\n0 - Exit\nEnter command number: ")
    os.system(clear_cmd)


    if stat == "1":
        if os.path.exists("./database/users.json"):
            User.dictionary = Human.json_import("./database/users.json")
        else:
            Human.json_save("./database/users.json", {})


        while 1:
            print("\n******** - Welcome to user management panel - ********\n")
            stat = input("Stat:\n1 - Sign Up\n2 - Sign In\n0 - Exit\nEnter command number: ")
            os.system(clear_cmd)


            # User sign up - Checked: OK.
            if stat == "1":
                print("\n********** ^ Sign up form ^ **********\n")
                fname = input("Enter First Name: ")
                lname = input("Enter Last Name: ")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                birth_date = input("Enter Birth date (YYYY/MM/DD): ")
                phone_number = input("Enter Phone number (e.g. 09876543210) : ")
                os.system(clear_cmd)
                try:
                    User.signup(
                        fname, lname, username, password, birth_date, phone_number
                    )
                except RepUserError:
                    os.system(clear_cmd)
                    print("\nUsername Already Taken! ")
                except ShortPasswordError:
                    os.system(clear_cmd)
                    print("\nToo Short Password! ")
                except PhoneNumberError:
                    os.system(clear_cmd)
                    print("Invalid phone number (e.g. 09876543210).")
                else:
                    os.system(clear_cmd)
                    print("\nSigning Up Completed! ")
        

            elif stat == "2":
                print("\n************** - Login form - **************\n")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                try:
                    user_object = User.sign_in_validation(username, password)
                except UserError:
                    os.system(clear_cmd)
                    print("\nUsername not Found! ")
                    continue
                except PasswordError:
                    os.system(clear_cmd)
                    print("\nWrong Password! ")
                    continue
                else:
                    os.system(clear_cmd)
                    print("\nSigning In Completed! ")

                while 1:
                    print("\n************ - User Dashboard - ************\n")
                    stat = input(
                        "State:\n1 - Show User Information\n2 - Edit user info\n3 - Show available Tickets\n4 - Reserve Ticket\n5 - Charge Wallet\n0 - Back to Main Menu: "
                    )
                    if stat == "1":
                        print(user_object)
                        print("List of Bank Accounts:")

                    elif stat == "2":
                        while 1:
                            print("\n***** ^ Edit User mode ^ *****\n")
                            stat = input(
                                "Stat 1(Edit profile) - 2(Password Change) - 3(Show Current Plan) - 4(Change Plan) - 5(Edit Bank Accounts) - 6(Back to Dashboard)   "
                            )

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

                            elif stat == "4":
                                print("***** ^ Change Plan ^ *****")

                            elif stat == "5":
                                print("***** ^ Edit Bank Accounts ^ *****")
                                print(
                                    "Stat 1(Add a Bank Account -\
                                        2(Edit Bank Accounts))"
                                )
                                if stat == "1":
                                    print("***** ^ Add Bank Account ^ *****")

                                elif stat == "2":
                                    print("***** ^ Edit Bank Accounts ^ *****")

                    elif stat == "3":
                        print("***** ^ Ticket Menu ^ *****")

                    elif stat == "4":
                        print("***** ^ Reserve Ticket ^ *****")

                    elif stat == "5":
                        print("***** ^ Wallet Charge Menu ^ *****")

                    elif stat == "0":
                        print("\nExiting User Panel...")
                        user_object.delete_user()
                        break

                    else:
                        print("\nInvalid State! ")
                        continue


            # Exit command - Checked: OK.
            elif stat == "0":
                os.system(clear_cmd)
                print("\nExiting the User Management Panel... ")
                break
            # Invalid State command - Checked: OK.
            else:
                os.system(clear_cmd)
                print("\nInvalid State! ")
                continue


    elif stat == "2":
        while 1:
            print("\n******** - admin management panel - ********\n")
            stat = input("Stat:\n1 - Sign In\n0 - Exit\nEnter command number:  ")
            os.system(clear_cmd)
            
            # Admin log in - Checked: OK.
            if stat == "1":
                print("\n************** - Login form - **************\n")
                try:
                    username = input("Enter Username: ")
                    password = getpass("Enter Password: ")
                    admin_object = Admin.sign_in_validation(username, password)
                except UserError:
                    os.system(clear_cmd)
                    print("\nUsername not Found! ")
                    continue
                except PasswordError:
                    os.system(clear_cmd)
                    print("\nWrong Password! ")
                    continue
                else:
                    os.system(clear_cmd)
                    print("\nSigning In Completed! ")
                    if os.path.isfile("./database/films.json"):
                        Film.films = Film.load_films_from_json()
                    else:
                        Film.save_films_to_json({})


                while 1:
                    print("\n************ - Admin Dashboard - ************\n")
                    stat = input(
                        "Stat:\n1 - Add film\n2 - Remove film\n3 - Add Ticket\n4 - Show Your Information\n5 - Edit Username\n6 - Password Change\n0 - Back to Main Menu\nEnter command number: "
                    )
                    os.system(clear_cmd)
                    # Add new film - Checked: OK.
                    if stat == "1":
                        print("\n************** ^ Add film ^ **************\n")
                        film_name = input("Film name: ")
                        film_genre = input("Film genre (e.g. Comedy/Action/Romance e.t.): ")
                        age_rate = input("Film age rating: ")
                        Admin.add_film(film_name, film_genre, age_rate)
                        os.system(clear_cmd)
                        print("\nFilm added successfully! \n")

                    # Remove film - Checked: OK.
                    elif stat == "2":
                        print("********** ^ Remove Film ^ **********")
                        film_name = input("Enter Film Name to Remove: ")
                        try:
                            Admin.remove_film(film_name)
                        except FilmError:
                            os.system(clear_cmd)
                            print("Film with this Name not found for Remove! ")
                            continue
                        else:
                            os.system(clear_cmd)
                            print("Film Removed Successfully! ")

                    # Add ticket - Checked: OK.
                    elif stat == "3":
                        print("***** ^ Add Ticket ^ *****")
                        film_name = input("Enter Film Name: ")
                        year, month, day = input("Enter scene date (YYYY-MM-DD): ").split("-")
                        film_date = datetime.date(int(year), int(month), int(day)).isoformat()
                        hour, minute = input("Enter Scene time (HH:MM): ").split(":")
                        scene_time = datetime.time(hour = int(hour), minute=int(minute)).isoformat(timespec="minutes")
                        ticket_capacity = int(input("Enter the Scene Capacity: "))
                        try:
                            Admin.add_show(film_name, film_date, scene_time, ticket_capacity)
                        except AddTicketFailed:
                            os.system(clear_cmd)
                            print("Incorrect data, please check information.")
                        else:
                            os.system(clear_cmd)
                            print("\nTicket Added Successfully! \n")

                    # Admin info - Checked: OK.
                    elif stat == "4":
                        os.system(clear_cmd)
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
                            os.system(clear_cmd)
                            print("\nUsername already Taken! ")
                        except PhoneNumberError:
                            os.system(clear_cmd)
                            print("Invalid Phone Number format! ")
                        else:
                            os.system(clear_cmd)
                            print("\nUser Information has been Updated! ")

                    # Change admin password - Checked: OK
                    elif stat == "6":
                        print("\n********** ^ Password Change ^ **********\n")
                        old_pass = getpass("Enter Old Password: ")
                        new_pass = getpass("Enter New Password: ")
                        rep_new_pass = getpass("Enter New Password again: ")
                        try:
                            admin_object.password_change(old_pass, new_pass, rep_new_pass)
                        except PasswordError:
                            os.system(clear_cmd)
                            print("\nWrong Old Password! ")
                        except TwoPasswordError:
                            os.system(clear_cmd)
                            print("\nTwo new passwords doesnt match! ")
                        except ShortPasswordError:
                            os.system(clear_cmd)
                            print("New Password is too short! ")
                        else:
                            os.system(clear_cmd)
                            print("\nYour Password has been changed! ")


                    # Exit command - Checked: OK
                    elif stat == "0":
                        os.system(clear_cmd)
                        print("\nExiting Admin Panel...")
                        admin_object.delete_admin()
                        break
                    # Invalid state command - Checked: OK
                    else:
                        os.system(clear_cmd)
                        print("\nInvalid State! ")
                        continue

            elif stat == "0":
                print("\nExiting the Admin Management Panel... ")
                break

            else:
                os.system(clear_cmd)
                print("\nInvalid State! ")
                continue

    elif stat == "0":
        os.system(clear_cmd)
        print("Exiting the program...")
        break

    else:
        os.system(clear_cmd)
        print("Invalid stat.")
        continue
