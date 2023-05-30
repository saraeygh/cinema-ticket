#! /usr/bin/python3

import datetime
import json
import os

class Film:
    """
    This class is for modeling film.
    """
    def __init__(self, name: str, genre: str, age_rating: str, tickets: dict):
        self.name = name
        self.genre = genre
        self.age_rating = age_rating
        self.tickets = tickets
        Film.films.update({self.name: self.__dict__})

    films = {}

    @classmethod
    def load_films_from_json(cls):
        """
        This class method is for loading our films and\
                tickets data in the dictionary\
                from a json file called database/films.json
        """
        with open("./database/films.json", mode="r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def save_films_to_json(cls, dictionary):
        """
        This class method is for saving our films and\
                tickets data in the dictionary\
                into a json file called database/films.json
        """
        with open("./database/films.json", mode="w+", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4)

    @classmethod
    def add_film(cls, name: str, genre: str,
                 age_rating: str, scene_date, showtime, capacity):
        """
        This class method is for adding a film and its ticket.
        """
        cls(name, genre, age_rating, Ticket.ticket_dict)
        Ticket(name, scene_date, showtime, capacity)

    @classmethod
    def get_object(cls, name):
        """
        This class method is for getting the film name\
                and creating a object from that information\
                for us.
        """
        for i, j in Film.films.items():
            if i == name:
                return cls(j["name"],
                           j["genre"],
                           j["age_rating"],
                           j["tickets"])

    @classmethod
    def remove_film(cls, name: str):
        """
        This class method is for removing\
                a film fro our database.
        """
        for film in Film.films:
            if film == name:
                del Film.films[name]
                cls.save_films_to_json(Film.films)
                break


class Ticket(Film):
    """
    This class is for modeling Ticket
    """

    ticket_dict = {}

    def __init__(self, name, scene_date, showtime, capacity):
        self.name = name
        self.scene_date = scene_date
        self.showtime = showtime
        self.available_seats = capacity
        Ticket.ticket_dict.update({f"{self.scene_date} _ {self.showtime}": self.__dict__})
        for film, info in Film.films.items():
            if film == self.name:
                info["tickets"] = Ticket.ticket_dict
        Film.save_films_to_json(Film.films)

    @staticmethod
    def add_ticket(name, scene_date, showtime, capacity):
        """
        This method is for adding a ticket from a defined film
        """
        return Ticket(name, scene_date, showtime, capacity)

    def sell_ticket(self, quantity):
        """
        This method is for seeling ticket\
                taking us count and substraction this\
                count from our total quantity of that\
                ticket
        """
        if quantity <= self.available_seats:
            self.available_seats -= quantity
            Ticket.ticket_dict["capacity"] = self.available_seats
            Film.films[self.name]["tickets"]["capacity"] = self.available_seats
            Film.save_films_to_json(Film.films)
            print(f"{quantity} ticket(s) sold successfully.")
        else:
            print("Insufficient available seats.")


while True:
    if os.path.isfile("database.json"):
        Film.films = Film.load_films_from_json()
    else:
        Film.save_films_to_json({})

    print("1. Add Film")
    print("2. Remove Film")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        film_name = input("Enter film name: ")
        film_genre = input("Enter film genre (Comedy/Action/Family/Romance): ")
        age_rate = int(input("Enter film age rating: "))
        year, month, day = input("Enter the scene_date: ").split("-")
        film_date = datetime.date(int(year), int(month), int(day)).isoformat()
        hour, minute = input("Enter scene time: ").split(":")
        scene_time = datetime.time(hour=int(hour), minute=int(minute)).isoformat(timespec='minutes')

        ticket_capacity = int(input("Enter the scene capacity: "))

        Film.add_film(film_name, film_genre, age_rate,
                      film_date, scene_time, ticket_capacity)

        print("Film added successfully!")
        print()
    elif choice == 2:
        film_name = input("Enter film name to remove: ")
        Film.remove_film(film_name)
        print("Film removed successfully!")
        print()
    elif choice == 3:
        break
    else:
        print("Invalid choice. Please try again.")
        print()
