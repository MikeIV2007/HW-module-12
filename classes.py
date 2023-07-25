from collections import UserDict
from datetime import datetime, timedelta
from sanytize import sanitize_phone_number
import pickle

class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...
    

class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value= None
        self.value = value
   
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):

        sanytized_ph = sanitize_phone_number(value)

        if sanytized_ph == '':          
            self.__value = ''
            return self.__value
        self.__value = sanytized_ph
        return self.__value

class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value= None
        self.value = value
   
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        format_str = "%Y-%m-%d"
        try:
            birthday_datetime = datetime.strptime(str(value), format_str).date()
            self.__value = birthday_datetime
            return self.__value
            
        except:
            self.__value= None
            return self.__value
        
        
class Record:
    
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        if phone == None:
            self.phones = phone
        else:
            self.phones = []
            self.phones.append(phone)
        self.birthday = birthday

    
    def add_phone(self, phone: Phone):
        if self.phones == None:
            self.phones = []
            self.phones.append(phone)
        if self.phones == None or phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"\nPhone number {phone} to contact {self.name} is added successfully!"
        return f"\nThe phone number {phone} for {self.name} is already in adress book!"
    

    def delete_pone(self, phone_to_delete):
        for phone in self.phones:
            if phone.value == phone_to_delete.value:
                self.phones.remove(phone)
                return f'\nPhone number {phone.value} for {self.name} removed successfully!'
        return f"\nPhone {phone_to_delete} not in the phones list of the contact {self.name}"
    
    def add_birthday(self, birthday: Birthday):

        if self.birthday == None:
            self.birthday = birthday
            return f"\nBirthday {self.birthday.value} to contact {self.name} is added successfully!"
        return f"\nThe {birthday} for {self.name} is already in adress book!"
    
    def days_to_birthday(self):

        date_now = datetime.now().date()
        birthday_this_year = datetime(date_now.year, self.birthday.value.month, self.birthday.value.day).date()
        delta = (birthday_this_year - date_now).days

        if delta > 0:
            return f'\n{delta} days until the next birthday of {self.name}'
        elif delta == 0:
            return f'\n{self.name} birthday is today!'
        else:
            birthday_next_year = datetime(date_now.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            delta = (birthday_next_year - date_now).days
            return f'\n{delta} days until the next birthday of {self.name}'
        
    def __str__(self) -> str:
       
        if (self.phones == None or self.phones == []) and self.birthday == None:
            return f"{self.name}; Unknown; Uncknown"
        if self.phones == None or self.phones == []:
            return f"{self.name}; Unknown; {self.birthday.value}"
        if self.birthday == None:
            return f"{self.name}; {', '.join(str(p) for p in self.phones)}; Unknown"
        return f"{self.name}; {', '.join(str(p) for p in self.phones)}; {str(self.birthday.value)}"


class AddressBook(UserDict):

    def load_data(self):
        try:
            with open('address_book.bin', "rb") as file:
                self.data = pickle.load(file)
                print ('\nAddress book loaded successfully!')
                print (self.data)
        except FileNotFoundError:
            print ('\nAddress book is empty!')

    
    def save_data(self):
  
        with open('address_book.bin', "wb") as file:
            print ('\nAll data saved successfully!')
            pickle.dump(self.data, file)

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        self.save_data()
        return f"\nContact <<< {record} >>> added successfully!"
    
    def iterator(self, n):

        count = 0
        data_list = []
        for name, record in self.data.items():
            user_data = []
            user_name = name
            if record.birthday:
                user_birthday = record.birthday.value
            else:
                user_birthday = 'Unknown'

            phones_str = 'Unknown'
            user_phones_list = []
            user_phones= record.phones
            if record.phones != None:
                for phone in user_phones:
                    user_phones_list.append(phone.value)
                phones_str = ' ,'.join(user_phones_list)
            user_data = [user_name, phones_str, user_birthday]
            data_list.append(user_data)
            count += 1
            if count >= n:

                yield data_list
                count = 0
                data_list = []

        if data_list:
            yield data_list

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
    
if __name__ == '__main__':
    name = Name ('bill')
    #phone = "38050-111-22-22"
    phone = "    +38(050)123323"
    #phone = "     0503451234"
    #phone = ' 1234567891111234'
    phone = Phone(phone)
    print (phone.value)



    # #birthday = Birthday('2000-12-15')
    # birthday = Birthday('2000-12-1')
    # #print (name)
    # print (birthday.value)
    # print (type(birthday.value))
    # print (str(birthday.value))
    # record = Record('bill', birthday = birthday )
    # print('153', record.birthday)
    # print(record.days_to_birthday())

            
    # phone_1 = Phone(None)
    # print ('125', phone_1)

    """    # Bill +380(67)333-43-54
    #     name_1 = Name('Bill')
    #     print ('123', name_1)
    #     phone_1 = Phone('+380(67)333-43-54')
        phone_1 = Phone(None)
        print ('125', phone_1)
    #     #birthday = Birthday('2000-12-15')
    #    #birthday = Birthday('2000-07-18')
    #     birthday = Birthday('2000-07-17')
    #     print ('129', birthday)
    #     record_1 = Record(name_1, phone_1, birthday)
    #     print ('131', record_1)
    #     print ('132', record_1.birthday.value)
    #     address_book = AddressBook()
    #     address_book.add_record(record_1)
    #     print ('134', address_book)
    #     print ('135', record_1.days_to_birthday())"""
