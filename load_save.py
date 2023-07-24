import pickle
from classes import AddressBook

def load_data():
    try:
        with open('address_book.bin', "rb") as file:
            pickle.load(address_book, file)
            print ('\nAddress book loaded successfully!')
    except FileNotFoundError:
        print ('\nAddress book is empty!')

    
def save_data()-> None:
    with open('address_book.bin', "wb") as file:
        print ('\nAll data saved successfully!')
        address_book = pickle.dump(file)