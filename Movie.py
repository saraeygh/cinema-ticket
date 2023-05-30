from abc import ABC, abstractmethod
import datetime
import json
import os
from zoneinfo import available_timezones

class Film(ABC):
    """
    A class to define the film, which is conducted by the admin

    """
    def __init__(self, name: str, genre: str, age_rating: str, tickets: dict = {}):
        self.name = name
        self.genre = genre
        self.age_rating = age_rating
        self.tickets = tickets
        Film.films.update({self.name: self.__dict__})
        
    films = {}

    @classmethod
    def load_films_from_json(cls):
        """
        Function to load the json file if it exists
        """
        #try:
        with open("database.json", 'r') as file:
            return json.load(file)
        #except FileNotFoundError:
        #    self.films = {}

    @classmethod
    def save_films_to_json(cls, dictionary):
        """
        If the json file does not exist, this function will create a json file

        """
        with open("database.json", 'w+') as file:
            json.dump(dictionary, file, indent=4)


    @classmethod
    def add_film(cls, name: str, genre: str, age_rating: str, scene_date, showtime, capacity):
        """
        A function to add a movie that includes the name, genre, age range, showtime, capacity
        """

        film = cls(name, genre, age_rating)
        ticket = Ticket(name, scene_date, showtime, capacity)

     
    @classmethod
    def get_object(cls, name):
        """
        Function to create an object from the movie
        """

        for i, j in Film.films.items():
            if i == name:
                return cls(j["name"],
                            j["genre"],
                            j["age_rating"],
                            j["scene_date"],
                            j["scene_time"],
                            j["capacity"])

    @classmethod   
    def remove_film(cls, name: str):
        """
        Movie delete function
        """

        for film in Film.films:
            if film == name:
                del Film.films[name]
                cls.save_films_to_json(Film.films)
                break


class Ticket(Film):
    ticket_dict = {}
    def __init__(self, name, scene_date, showtime, capacity):
        #super().__init__(name, genre, age_rating)
        self.name = name
        self.scene_date = scene_date
        self.showtime = showtime
        self.available_seats = capacity
        Ticket.ticket_dict.update({f"{self.scene_date} _ {self.showtime}": self.__dict__})
        for film in Film.films:
            if film == self.name:
                Film.films[film]["tickets"] = Ticket.ticket_dict
        Film.save_films_to_json(Film.films)

    @staticmethod
    def add_ticket(name, scene_date, showtime, capacity):
        """
        Function to create ticket for user purchase
        """

        return Ticket(name, scene_date, showtime, capacity)
    

    def sell_ticket(self, quantity):
        """
        Function to sell tickets
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
        name = input("Enter film name: ")
        genre = input("Enter film genre (Comedy / Action / Family / Romance): ")
        
        try:
            age_rating = int(input("Enter film age rating: "))
        except ValueError:
            print("*Please enter your age in the number!*\n")
            continue

        try:
            year, month, day = input("Enter the scene_date of release of the movie(YYYY-MM-DD): ").split("-")
        except ValueError:
            print("*sorry! Enter the release date of the movie as YYYY-MM-DD*\n")
            continue

        scene_date = datetime.date(int(year), int(month), int(day)).isoformat()
        
        try:
            hour , minute = input("Enter hour and minute(HH:MM): ").split(":")
        except ValueError:
            print("*Enter the exact time of the movie as HH:MM*\n")
            continue

        scene_time = datetime.time(hour=int(hour), minute=int(minute)).isoformat(timespec='minutes')
        
        try:
            capacity = int(input("Enter the capacity of the movie theater: "))
        except ValueError:
            print("*Please enter your age in the number!*\n")
            continue

        Film.add_film(name, genre, age_rating, scene_date, scene_time, capacity)
        print("Film added successfully!")
        print()
    elif choice == 2:
        name = input("Enter film name to remove: ")
        Film.remove_film(name)
        print("Film removed successfully!")
        print()
    elif choice == 3:
        break
    else:
        print("Invalid choice. Please try again.")
        print()

        
