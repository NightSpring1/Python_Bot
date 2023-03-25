from classes import Name, Phone, Record, AddressBook


def input_error(func):
    def execute(*args):
        try:
            return func(*args)
        except IndexError:
            return 'IndexError'
        except ValueError:
            return 'ValueError'
        except KeyError:
            return 'KeyError'

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
    show: shows all contacts (to be done with iterator in 11hw)
    '''
    return message


@input_error
def add_handler(addressbook: AddressBook, *args) -> str:
    name = Name(args[0])
    phone = Phone(args[1]) if len(args) > 1 else None
    record = Record(name, phone)
    if name.value in addressbook.data:
        addressbook[name.value].phones = phone
    else:
        addressbook.add_record(record)
    return 'Record added'


@input_error
def show_handler(addressbook: AddressBook, *args) -> str:
    message = addressbook.show_records()
    return message


@input_error
def change_handler(addressbook: AddressBook, *args) -> str:
    del addressbook[args[0].capitalize()][Phone(args[1])]
    addressbook[args[0].capitalize()].phones = Phone(args[2])
    return 'Phone was changed'


@input_error
def del_handler(addressbook: AddressBook, *args):
    if args[0].lower() == 'phone':
        del addressbook[args[1].capitalize()][Phone(args[2])]
        message = 'Phone Was removed'
    elif args[0].lower() == 'record':
        addressbook.del_record(args[1].capitalize())
        message = 'Record was removed'
    else:
        message = f"del does not support {args[0]} argument."
    return message


function = {'hello': welcome_message,
            'help': help_message,
            'add': add_handler,
            'show': show_handler,
            'change': change_handler,
            'del': del_handler}
