#! /usr/bin/python3

from getpass import getpass
from os import path
from movie import Film, Ticket
import datetime
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

while 1:
    print("\n***** - Welcome to cinema Ticket - *****")
    stat = input("Stat (1(User mode) - 2(Admin mode)) - 0(Exit)   ")
    if stat == "1":
        if path.exists("./database/users.json"):
            User.dictionary = Human.json_import("./database/users.json")
        else:
            Human.json_create("./database/users.json")

        while 1:
            print("\n******** - Welcome to user management panel - ********\n")
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
                    print("\n************ - User Dashboard - ************\n")
                    stat = input("Stat (1(Show User Information) - 2(Edit)\
                            - 3(Password Change) - 4(Back to Main Menu)):   ")
                    if stat == "1":
                        print(user_object)

                    elif stat == "2":
                        print("\n***** ^ Edit User information mode ^ *****\n")
                        print("abort change any item, leave it and Enter.\n")
                        try:
                            new_usr = input("Enter New Username: ")
                            new_ph_numb = input("New Phone Number: ")
                            user_object.edit_user(new_usr, new_ph_numb)
                        except RepUserError:
                            print("\nUsername already Taken! ")
                        else:
                            print("\nUser Information has been Updated! ")

                    elif stat == "3":
                        print("\n********** ^ Password Change ^ **********\n")
                        try:
                            old_p = getpass("Old Password: ")
                            new_p = getpass("New Password: ")
                            re_new_p = getpass("New Password again: ")
                            user_object.password_change(old_p, new_p, re_new_p)
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
        if path.exists("./database/admins.json"):
            Admin.dictionary = Human.json_import("./database/admins.json")
        else:
            Human.json_create("./database/admins.json")

        while 1:
            print("\n******** - admin management panel - ********\n")
            print()
            stat = input("Stat (0(Exit) - 1(Sign Up) - 2(Sign In)):   ")

            if stat == "1":
                print("\n********** ^ Sign up form ^ **********\n")
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                try:
                    Admin.signup(username, password)
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
                    admin_object = Admin.sign_in_validation(username, password)
                except UserError:
                    print("\nUsername not Found! ")
                    continue
                except PasswordError:
                    print("\nWrong Password! ")
                    continue
                else:
                    print("\nSigning In Completed! ")
                    if path.isfile("./database/films.json"):
                        Film.films = Film.load_films_from_json()
                    else:
                        Film.save_films_to_json({})

                while 1:
                    print("\n************ - Admin Dashboard - ************\n")
                    stat = input("Stat (1(Add film) - 2(Remove film)\
                            - 3(Show User Information) - 4(Edit Profile)\
                            - 5(Password Change) - 6(Back to Main Menu)):   ")
                    if stat == "1":
                        print("\n************** ^ Add film ^ **************\n")
                        film_name = input("Enter Film name: ")
                        film_genre = input("Enter Film Genre (Comedy/Action/Family/Romance): ")
                        age_rate = input("Enter film Age Rating: ")
                        year, month, day = input("Enter scene date (YYYY-MM-DD): ").split("-")
                        film_date = datetime.date(int(year), int(month), int(day)).isoformat()
                        hour, minute = input("Enter Scene time (HH:MM): ")
                        scene_time = datetime.time(hour=int(hour), minute=int(minute)).isoformat(timespec='minutes')
                        ticket_capacity = int(input("Enter the Scene Capacity: "))
                        Film.add_film(film_name, film_genre, age_rate,
                                      film_date, scene_time, ticket_capacity)
                        print("\nFilm added successfully! \n")

                    elif stat == "2":
                        print("********** ^ Remove Film ^ **********")
                        film_name = input("Enter Film Name to Remove: ")
                        try:
                            Film.remove_film(film_name)
                        except FilmError:
                            print("Film with this Name not found for Remove! ")
                        else:
                            print("film Removed Successfully! ")

                    elif stat == "3":
                        print(admin_object)

                    elif stat == "4":
                        print("********** ^ admin Edit profile ^ **********")
                        print("abort change any item, leave it and Enter.\n")
                        try:
                            new_username = input("Enter New Username: ")
                            admin_object.edit_user(new_username)
                        except RepUserError:
                            print("\nUsername already Taken! ")
                        else:
                            print("\nUser Information has been Updated! ")

                    elif stat == "5":
                        print("\n********** ^ Password Change ^ **********\n")
                        try:
                            old_pass = getpass("Enter Old Password: ")
                            new_pass = getpass("Enter New Password: ")
                            rep_new_pass = getpass("Enter New Password again: ")
                            admin_object.password_change(old_pass, new_pass, rep_new_pass)
                        except PasswordError:
                            print("\nWrong Original Password! ")
                        except TwoPasswordError:
                            print("\nTwo new passwords are not matched! ")
                        except ShortPasswordError:
                            print("Two Short New Password! ")
                        else:
                            print("\nYour Password has been changed! ")

                    elif stat == "6":
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
