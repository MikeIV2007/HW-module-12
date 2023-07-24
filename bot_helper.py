import re
from rich import print
from rich.table import Table
from classes import AddressBook, Name, Phone, Record, Birthday
#import pickle

I = 1

address_book = AddressBook()

def table_of_commands():
    table = Table(title='\nALL VALID COMMANDS:\nAll entered data must be devided by gap!\n* Phone number must have 10 or 12 digits!')
    table.add_column('COMMAND', justify='left')
    table.add_column('NAME', justify='left')
    table.add_column('PHONE NUMBER', justify='letf')
    table.add_column('BIRTHDAY', justify='center')
    table.add_column('DESCRIPTION', justify='left')
    table.add_row('hello', '-', '-', '-', 'Greeting')
    table.add_row('add', 'Any name ', 'Phone number *', '-', 'Add new contact')
    table.add_row('append', 'Existing name', 'Additional phone number *', '-', 'Append phone number') 
    table.add_row('delete', 'Existing name', 'Phone to delete *', '-', 'Delete phone number')
    table.add_row('birthday', 'Existing name', '-', 'YYYY-MM-DD', 'Add birthday')
    table.add_row('days to birthday', 'Existing name', '-', '-', 'Sow days to birthday')
    table.add_row('phone', 'Existing name', '-', '-', 'Getting phone number')
    table.add_row('show all / show all N', '-', '-', '-', 'Getting Address Book/ N - quantity of records on th page')
    table.add_row('good bye / close / exit', '-', '-', '-', 'Exit')
    table.add_row('help', '-', '-', '-','Printing table of commands')

    return table


# def load_data():
#     try:
#         with open('address_book.bin', "rb") as file:
#             pickle.load(address_book, file)
#             print ('\nAddress book loaded successfully!')
#     except FileNotFoundError:
#         print ('\nAddress book is empty!')

    
# def save_data()-> None:
#     with open('address_book.bin', "wb") as file:
#         print ('\nAll data saved successfully!')
#         address_book = pickle.dump(file)


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        
        except IndexError as e:
            error_message = f"IndexError: {str(e)}"
            return error_message
    return wrapper


@input_error
def add_command(*args):
    if args[0] == '':
        return '\nMissing mame of contact!'

    name = Name(args[0])
    if args[1] == "":
        return f'\nPhone number is missing!'
    
    phone = Phone(args[1])
    
    if phone.value == '':
        return f'\nPhone number {args[1]} is hot correct!\nPhone must have 10 or 12 digites!'
    
    rec: Record = address_book.get(str(name))

    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


def delete_phone_command(*args):
    if args[0] == '':
        return '\nMissing mame of contact!'
    
    name = Name(args[0])
    phone_to_delete = Phone (args[1])
    record: Record = address_book.get(str(name))

    if record:
        return record.delete_pone(phone_to_delete)
    return f'\nContact {name} not found in address book!'


def phone_command(*args):
    if args[0] == '':
        return '\nMissing name of contact!'

    for name, record in address_book.data.items():
        if name == args[0]:
            if record.phones == []:
                return (f'\nContact {name} doesn\'t have any phone!')
            phones = ", ".join(str(phone) for phone in record.phones)
            return (f'\nPhone number(s) of {name} is(are): {phones}')
    return f'\nContact {args[0]} not found in address book!'


def exit_command(*args):
    return '\nGood bye! Have a nice day!\n'


def show_all_command(*args):

    if len(address_book.data) == 0:
        return '\nAddress Book is empty!'
    
    n = 5
    k = 1

    try:
        n = int(args[0])
    except ValueError:
        print (f'\nEnterd number of pages <<< {args[0]} >>> does not represent a valid integer!\nDefault number of records N = {n} will be used')

    for block in address_book.iterator(n):
        
        table = Table(title=f'\nADDRESS BOOK page {k}')
        table.add_column('Name', justify='left')
        table.add_column("Phone number", justify="left")
        table.add_column("Birthday", justify="left")
        for item in block:
            table.add_row(str(item[0]), str(item[1]), str(item[2]) )
        print (table)
        k += 1

    return "\nEnd of address book"


def help_command(*args):
    return table_of_commands()


def hello_command(*args):
    return '\nHow can I help you?'

def birthday_command(*args):
    if args[0] == '':
        return '\nMissing mame of contact!'

    name = Name(args[0])
    birthday = Birthday(args[1])

    if birthday.value == None:
        return f'\nBirthday {args[1]} is not correct!'
    rec: Record = address_book.get(str(name))

    if rec:
        return rec.add_birthday(birthday)
    rec = Record(name, birthday = birthday)
    return address_book.add_record(rec)


def days_to_birthday_command(*args):

    if args[0] == '':
        return '\nMissing mame of contact!'
    for name, record in address_book.data.items():
        if name == args[0]:
            record: Record = record
            return record.days_to_birthday()
    

COMMANDS = {
    add_command: ('add', 'append'),
    phone_command: ('phone',),
    delete_phone_command: ('delete',),
    exit_command: ('good bye', 'close', 'exit'),
    show_all_command: ('show all',),
    help_command: ('help',),
    hello_command: ('hello',),
    birthday_command: ('birthday',),
    days_to_birthday_command: ('days to birthday',)
}


def get_user_name(user_info: str )-> tuple:

    regex_name = r'[a-zA-ZА-Яа-я]+'
    user_input_split = user_info.strip().split()
    name_list =[]

    for i in user_input_split:
        match_name = re.match(regex_name, i)
        if match_name:
            if len(match_name.group()) == len(i):
                name_list.append(i.capitalize())
                user_info = user_info[match_name.span()[1]:].strip()
                user_data = user_info
            else:
                return '\nName is not correct! Try again!'


    if len(name_list)>=1:
        name = ' '.join(name_list)
    else:
        name = ''
        user_data = ''

    return name, user_data

def parser(text:str):
    for command, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                user_info = text[len(kwd):].strip()
                return command, user_info
            
    print ('\nUnknown command! Try againe!')
    command = None
    user_info = None
    return command, user_info


def main():

    global I
    if I == 1:
        address_book.load_data()
        print (table_of_commands())
        I += 1

    while True:
 
        user_input = (input(f'\nEnter command, please!\n\n>>>')).strip()
        
        command, user_info = parser(user_input)

        if command == None:
            continue
        if len(user_info) > 0:

            if COMMANDS[command][0] == 'birthday':
                name, birthday = get_user_name(user_info)
                if len(birthday)>0:
                    data = (name, birthday)
                else:
                    birthday = None
                    data = (name, birthday)

            elif COMMANDS[command][0] == 'show all':     
                data = (user_info,)

            else:
                name, phone = get_user_name(user_info)
                if len (phone) > 0:
                    phone = phone
                    data = (name, phone)
                else:
                    phone = ''
                    data = (name, phone)
        else:
            name = ''
            phone = ''
            data = (name, phone)

        result = command(*data)
        print(result)
        
        if command == exit_command:
            break

if __name__ == "__main__":
    main()

# add Bill +380673334354
# add Billy +380673331111
# add Bill Jonson +380(67)333-99-88
# add Bil +380673334354
# add Bi +380673331111
# add Bill Jonson +380(67)333-99-88
# add Bill Jonso +380(67)333-99-88
# add Bill Jons +380(67)333-99-88
# add Bill Jon +380(67)333-99-88
# add Bill Jo +380(67)333-99-88
# add Bill J +380(67)333-99-88
# add Mike Jonn +380(67)111-41-77
# add Mike +380(67)111-41-77

# show all
# help
# phone
# add Bill
# ADD Bill +380(67)333-43-5
# ADD Bill +380673334354
# Append Bill +380673331111
# add
# BirthDaY Bill 2002-05-32 #not correct
# BirthDaY Bill 2002-05-30
# Days To Birthday Bill
# DeLete Bill +380(67)333-43-54
# ADD Bill Jonson +380(67)333-43-5
# Append Bill Jonson +380(67)333-99-88
# PhoNE Bill Jonson
# DeleTe Bill Jonson +380(67)333-43-5
# +380(67)282-8-313
# CHange Mike Jonn +380(67)111-41-77
# delete Mike Jonn +380(67)111-41-77
# PHONE Mike Jonn +380(67)111-41-77
# CHange Bill Jonson +380(67)111-41-77
# PHONE Bill
# phone Bill +380(67)333-43-54
# 12m3m4n
# 12me3m3m 123m3mm2
# ADD Jill Bonson +380(67)333-43-54
# PhOnE Jill Bonson +380(67)333-43-54
# ADD Jill +380(67)333-43-54
# append Jill +380(67)222-44-55
# Иванов Иван Иванович +380(67)222-33-55
# append Иванов Иван Иванович +380(67)999-1-777
# phone Иванов Иван Иванович 
# delete Иванов Иван Иванович +380(67)222-33-55
# dfsadfads asdgfas ref asdf     TypeError
# Jgfdksaflf Sdfjldsf; Asdfk;;lsdff Jldsf;sf';; sdff ; jldsf;sF';;
# add mike 123123-12-3
# delete mike 123123-12-3
# phone mike 123123-12-3