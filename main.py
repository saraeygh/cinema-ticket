#! /usr/bin/python3

import datetime
from getpass import getpass
import os
from movie import Film, Ticket
from custom_exceptions import (
        UserError,
        RepUserError,
        PasswordError,
        TwoPasswordError,
        ShortPasswordError,
        FilmError,
        NoCapacityError
        )

from human import Human, User, Admin

if not os.path.isdir("./database"):
    os.mkdir("./database")

while 1:
    print("\n***** - Welcome to cinema Ticket - *****")
    stat = input("Stat (1(User mode) - 2(Admin mode)) - 0(Exit)   ")
    if stat == "1":
        if os.path.exists("./database/users.json"):
            User.dictionary = Human.json_import("./database/users.json")
        else:
            Human.json_save("./database/users.json", {})

        while 1:
            print("\n******** - Welcome to user management panel - ********\n")
            stat = input("Stat (0(Exit) - 1(Sign Up) - 2(Sign In)):   ")

            if stat == "1":
                print("\n********** ^ Sign up form ^ **********\n")
                fname = input("Enter First Name: ")
                lname = input("Enter Last Name: ")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                birth_date = input("Enter Birth date (YYYY/MM/DD): ")
                phone_number = input("Enter Phone number(Optional): ")
                try:
                    User.signup(fname, lname, username,
                                password, birth_date,
                                phone_number)
                except RepUserError:
                    print("\nUsername Already Taken! ")
                except ShortPasswordError:
                    print("\nToo Short Password! ")
                else:
                    print("\nSigning Up Completed! ")
            elif stat == "2":
                print("\n************** - Login form - **************\n")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                try:
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
                    print("\n************ - User Dashboard - ************\n")
                    stat = input("Stat (1(Show User Information) - 2(Edit) - 3(Show Tickets menu) - 4(Reserve Ticket) - 5(Cahrge Wallet) - 6(Back to Main Menu)):   ")
                    if stat == "1":
                        print(user_object)
                        print("List of Bank Accounts:")
                    
                    elif stat == "2":
                        while 1:
                            print("\n***** ^ Edit User mode ^ *****\n")
                            stat = input("Stat 1(Edit profile) - 2(Password Change) - 3(Show Current Plan) - 4(Change Plan) - 5(Edit Bank Accounts) - 6(Back to Dashboard)   ")
    
                            if stat == "1":
                                print("\n***** ^ Edit Profile mode ^ *****\n")
                                print("For Abort to editing any item, just leave it and press Enter.")
                                new_fname = input("Enter New First Name: ")
                                new_lname = input("Enter New Last Name: ")
                                new_b_date = input("Enter New Birth Date (YYYY-MM-DD): ")
                                new_usr = input("Enter New Username: ")
                                new_ph_numb = input("New Phone Number: ")
                                try:
                                    user_object.edit_user(new_fname, new_lname,
                                                          new_usr, new_ph_numb,
                                                          new_b_date)
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
                                    user_object.password_change(old_p,
                                                                new_p, re_new_p)
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
                                print("Stat 1(Add a Bank Account -\
                                        2(Edit Bank Accounts))")
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

                    elif stat == "6":
                        print("\nExiting User Panel...")
                        user_object.delete_user()
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

    elif stat == "2":
        if os.path.exists("./database/admins.json"):
            Admin.dictionary = Human.json_import("./database/admins.json")
        else:
            Human.json_save("./database/admins.json", {})

        while 1:
            print("\n******** - admin management panel - ********\n")
            print()
            stat = input("Stat (0(Exit) - 1(Sign In)):   ")

            if stat == "1":
                print("\n************** - Login form - **************\n")
                try:
                    username = input("Enter Username: ")
                    password = getpass("Enter Password: ")
                    admin_object = Admin.sign_in_validation(username, password)
                except UserError:
                    print("\nUsername not Found! ")
                    continue
                except PasswordError:
                    print("\nWrong Password! ")
                    continue
                else:
                    print("\nSigning In Completed! ")
                    if os.path.isfile("./database/films.json"):
                        Film.films = Film.load_films_from_json()
                    else:
                        Film.save_films_to_json({})

                while 1:
                    print("\n************ - Admin Dashboard - ************\n")
                    stat = input("Stat (1(Add film) - 2(Remove film) - 3(Add Ticket) - 4(Show Your Information) - 5(Edit Username) - 6(Password Change) - 7(Back to Main Menu)):   ")
                    if stat == "1":
                        print("\n************** ^ Add film ^ **************\n")
                        film_name = input("Enter Film name: ")
                        film_genre = input("Enter Film Genre (Comedy/Action/Family/Romance): ")
                        age_rate = input("Enter film Age Rating: ")
                        Admin.add_film(film_name, film_genre, age_rate)
                       print("\nFilm added successfully! \n")

                    elif stat == "2":
                        print("********** ^ Remove Film ^ **********")
                        film_name = input("Enter Film Name to Remove: ")
                        try:
                            Film.remove_film(film_name)
                        except FilmError:
                            print("Film with this Name not found for Remove! ")
                        else:
                            print("Film Removed Successfully! ")

                    elif stat == "3":
                        print("***** ^ Add Ticket ^ *****")
                        film_name = input("Enter Film Name")
                        year, month, day = input("Enter scene date (YYYY-MM-DD): ").split("-")
                        film_date = datetime.date(int(year), int(month), int(day)).isoformat()
                        hour, minute = input("Enter Scene time (HH:MM): ")
                        scene_time = datetime.time(hour=int(hour), minute=int(minute)).isoformat(timespec='minutes')
                        ticket_capacity = int(input("Enter the Scene Capacity: "))
                        try:
                            Admin.add_show(film_name, film_date, scene_time, ticket_capacity)
                        except Exception:
                            print("Invalid truncation, please Try again.")
 

                    elif stat == "4":
                        print(admin_object)

                    elif stat == "5":
                        print("********** ^ admin Edit Username ^ **********")
                        print("abort change any item, leave it and Enter.\n")
                        new_username = input("Enter New Username: ")
                        try:
                            admin_object.edit_user(new_username)
                        except RepUserError:
                            print("\nUsername already Taken! ")
                        else:
                            print("\nUser Information has been Updated! ")

                    elif stat == "6":
                        print("\n********** ^ Password Change ^ **********\n")
                        old_pass = getpass("Enter Old Password: ")
                        new_pass = getpass("Enter New Password: ")
                        rep_new_pass = getpass("Enter New Password again: ")
                        try:
                            admin_object.password_change(old_pass, new_pass, rep_new_pass)
                        except PasswordError:
                            print("\nWrong Original Password! ")
                        except TwoPasswordError:
                            print("\nTwo new passwords are not matched! ")
                        except ShortPasswordError:
                            print("Two Short New Password! ")
                        else:
                            print("\nYour Password has been changed! ")

                    elif stat == "7":
                        print("\nExiting Admin Panel...")
                        admin_object.delete_admin()
                        break

                    else:
                        print("\nInvalid State! ")
                        continue

            elif stat == "0":
                print("\nExiting the Admin Management Panel... ")
                break

            else:
                print("\nInvalid State! ")
                continue

    elif stat == "0":
        print("Exiting the program...")
        break
