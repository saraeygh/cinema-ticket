import json

class Film:
    def __init__(self, file_path):
        self.file_path = file_path
        self.films = []

    def load_films_from_json(self):
        try:
            with open(self.file_path, 'r') as file:
                self.films = json.load(file)
        except FileNotFoundError:
            self.films = []

    def save_films_to_json(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.films, file, indent=4)

    def add_film(self, name, genre, age_rating):
        film = {
            'name': name,
            'genre': genre,
            'age_rating': age_rating
        }
        self.films.append(film)
        self.save_films_to_json()

    def remove_film(self, name):
        for film in self.films:
            if film['name'] == name:
                self.films.remove(film)
                self.save_films_to_json()
                break

class Ticket(Film):
    def __init__(self, name, genre, age_rating, capacity, showtime):
        super().__init__(name, genre, age_rating)
        self.capacity = capacity
        self.showtime = showtime
        self.available_seats = capacity

    def charge_ticket(self, quantity):
        if quantity <= self.available_seats:
            self.available_seats -= quantity
            print(f"{quantity} ticket(s) charged successfully.")
        else:
            print("Insufficient available seats.")

    def sell_ticket(self, quantity):
        if quantity <= self.available_seats:
            self.available_seats -= quantity
            print(f"{quantity} ticket(s) sold successfully.")
        else:
            print("Insufficient available seats.")

   

film_manager = Film('films.json')
film_manager.load_films_from_json()

while True:
    print("1. Add Film")
    print("2. Remove Film")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        name = input("Enter film name: ")
        genre = input("Enter film genre (Comedy / Action / Family / Romance): ")
        age_rating = int(input("Enter film age rating: "))
        film_manager.add_film(name, genre, age_rating)
        print("Film added successfully!")
        print()
    elif choice == 2:
        name = input("Enter film name to remove: ")
        film_manager.remove_film(name)
        print("Film removed successfully!")
        print()
    elif choice == 3:
        break
    else:
        print("Invalid choice. Please try again.")
        print()



        
