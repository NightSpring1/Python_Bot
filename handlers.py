from classes import Name, Phone, Birthday, Record, AddressBook


def input_error(func):
    def execute(*args):
        try:
            return func(*args)
        except IndexError as index_error:
            return index_error
        except ValueError as value_error:
            return value_error
        except KeyError as key_error:
            return key_error
        except AttributeError as attribute_error:
            return attribute_error

    return execute


def welcome_message(*args) -> str:
    message = "Hi! How can i help you?"
    return message


def help_message(*args) -> str:
    message = '''
    Commands:
    hello: prints Hello Message!
    add "user name" "user phone" : adds contact to the storage, if record already exist, adds new phone
    change "user name" "old phone" "new phone": change existing number to a new one
    del phone "user name" "phone": removes specified phone from record
    del record "user name": removes record from address book
    show: shows all contacts 
    birthday "user name" "birthday": adds birthday to record (format: day-month-year). Changeable.
    save: saves all records to storage1.dat
    load: loads records from storage1.dat
    search "any number of keywords": searches keywords in records and shows records in which matches are found 
    '''
    return message


@input_error
def add_handler(addressbook: AddressBook, *args) -> str:
    name = Name(args[0])
    phone = Phone(args[1]) if len(args) > 1 else None
    record = Record(name, phone)
    if name.name in addressbook.data:
        addressbook[name.name].add_phone(phone)
        message = f'Phone {phone} was added to {name} record.'
    else:
        addressbook.add_record(record)
        message = f'{name} record was added.'
    return message


@input_error
def show_handler(addressbook: AddressBook, *args) -> str:
    message = ''
    for page_num, page in enumerate(addressbook.show_records(records_per_page=5), 1):
        message += f'Page {page_num}:\n'
        message += page
    return message


@input_error
def change_handler(addressbook: AddressBook, *args) -> str:
    if len(args) < 3:
        return 'Not enough arguments'
    name = args[0].capitalize()
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    addressbook[name].del_phone(old_phone)
    addressbook[name].add_phone(new_phone)
    return f'Phone in {name} record was changed from {old_phone} to {new_phone}.'


@input_error
def del_handler(addressbook: AddressBook, *args) -> str:
    if args[0].lower() == 'phone':
        name = args[1].capitalize()
        phone = Phone(args[2])
        addressbook[name].del_phone(phone)
        message = f'Phone {phone} was removed from {name} record.'
    elif args[0].lower() == 'record':
        name = args[1].capitalize()
        addressbook.del_record(name)
        message = f'{name} record was removed.'
    else:
        message = f"del does not support {args[0]} argument."
    return message


@input_error
def birthday_handler(addressbook: AddressBook, *args):
    name = args[0].capitalize()
    addressbook[name].set_birthday(Birthday(args[1]))
    return f'Birthday updated for {name} record.'


@input_error
def search_handler(addressbook: AddressBook, *args):
    search_string = '|'.join(args)
    message = f'Searching words {", ".join(args)} in records:\n'
    for page_num, page in enumerate(addressbook.show_records(search_pattern=search_string), 1):
        message += page
    return message


def save_data(addressbook: AddressBook, *args) -> str:
    addressbook.save_records_to_file('storage1.dat')
    return "Records have been saved."


def load_data(addressbook: AddressBook, *args) -> str:
    addressbook.read_records_from_file('storage1.dat')
    return "Records have been loaded."


function = {'hello': welcome_message,
            'help': help_message,
            'add': add_handler,
            'show': show_handler,
            'change': change_handler,
            'del': del_handler,
            'birthday': birthday_handler,
            'search': search_handler,
            'save': save_data,
            'load': load_data}
