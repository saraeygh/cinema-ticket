
import json
import os
import unittest
from movie import Film

class TestSaveFilmsToJson(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()