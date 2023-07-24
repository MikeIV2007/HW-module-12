import pickle
from random import randint

class Hotel:
    def __init__(self, name = None, rooms = None) -> None:
        self.name = name
        self.rooms = rooms
        pass

    def __str__(self):
        return f'{self.name}, {self.rooms}'


file_name = "hotels.bin"
hotels = {}


for i in range(10):
    hotel=Hotel(f"Hotel-{i}", randint(100, 500))
    hotels[str(hotel.name)] = hotel

with open(file_name, "wb") as f:
    pickle.dump(hotels, f)

with open(file_name, "rb") as f:
    load_hotels = pickle.load(f)
    
print(load_hotels)

for hotel ,rooms in load_hotels.items():
    print(hotel,rooms)