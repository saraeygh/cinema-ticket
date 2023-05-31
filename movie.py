#! /usr/bin/python3

import json
from custom_exceptions import FilmError, NoCapacityError


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
        Film.save_films_to_json(Film.films)

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
    def add_film(cls, name: str, genre: str, age_rating: str):
        """
        This class method is for adding a film and its ticket.
        """
        obj = cls(name, genre, age_rating, Ticket.ticket_dict)
        obj.delete_film_obj()

    @classmethod
    def get_object(cls, name):
        """
        This class method is for getting the film name\
                and creating a object from that information\
                for us.
        """
        for i, j in Film.films.items():
            if i == name:
                return cls(j["name"], j["genre"], j["age_rating"], j["tickets"])

    def delete_film_obj(self):
        del self

    @classmethod
    def remove_film(cls, name: str):
        """
        This class method is for removing\
                a film fro our database.
        """
        if name not in Film.films:
            raise FilmError("Film Not Found! ")
        del Film.films[name]
        cls.save_films_to_json(Film.films)


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
        Ticket.ticket_dict.update(
            {f"{self.scene_date} _ {self.showtime}": self.__dict__}
        )
        for film, info in Film.films.items():
            if film == self.name:
                info["tickets"] = Ticket.ticket_dict
        Film.save_films_to_json(Film.films)

    @staticmethod
    def add_ticket(name, scene_date, showtime, capacity):
        """
        This method is for adding a ticket from a defined film
        """
        t_obj = Ticket(name, scene_date, showtime, capacity)
        t_obj.delete_film_obj()

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
            raise NoCapacityError("Insufficient ticket! ")

    def delete_ticket_obj(self):
        del self
