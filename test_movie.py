
import json
import os
from custom_exceptions import FilmError, NoCapacityError
import unittest
from movie import Film , Ticket


class TestFilm(unittest.TestCase):
    def test_save_films_to_json(self):
        dictionary = {
            "film1": {
                "name":"film1",
                "genre": "Action",
                "age_rating": 20
            },
            "film2": {
                "name":"film2",
                "genre": "Comedy",
                "age_rating": 22
            }
        }

        Film.save_films_to_json(dictionary)
        self.assertTrue(os.path.exists("./database/films.json"))
        with open("./database/films.json", mode="r", encoding="utf-8") as file:
            content = json.load(file)
            self.assertEqual(content, dictionary)

        os.remove("./database/films.json")
    
  
    def test_load_films_from_json(self):   
        expected_dictionary = {
            "film1": {
                "genre": "Family",
                "year": 30
            },
            "film2": {
                "genre": "Comedy",
                "year": 33
            }
        }
        with open("./database/films.json", mode="w+", encoding="utf-8") as file:
            json.dump(expected_dictionary, file, indent=4)
        actual_dictionary = Film.load_films_from_json()
        self.assertEqual(actual_dictionary, expected_dictionary)


    def test_remove_film(self):
        name = "Film1"
        Film.films[name] = {"genre": "Action", "age_rating": "PG-13"}
        Film.remove_film(name)

        self.assertNotIn(name, Film.films)

def remove_film(cls,name):
    if name not in Film.films:
        raise FilmError("Film Not Found! ")
    del Film.films[name]
    cls.save_films_to_json(Film.films)

class TestTicket(unittest.TestCase):
    def test_add_ticket(self):
        name = "Ticket1"
        scene_date = "2022-01-01"
        showtime = "19:00"
        capacity = 100

        add_ticket(name, scene_date, showtime, capacity)
        self.assertTrue(len(Ticket.ticket_dict) == 0)

# تعریف کلاس فیک برای تست
class FakeTicketClass:
    ticket_dict = {}

    def __init__(self, name, scene_date, showtime, capacity):
        self.name = name
        self.scene_date = scene_date
        self.showtime = showtime
        self.capacity = capacity

    def delete_film_obj(self):
        pass
def add_ticket(name, scene_date, showtime, capacity):
    Ticket.ticket_dict.clear()
    t_obj = FakeTicketClass(name, scene_date, showtime, capacity)
    t_obj.delete_film_obj()

    

if __name__ == "__main__":
    unittest.main()

