from classes import Name, Phone, Record, AddressBook


def input_error(func):
    def execute(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Please enter valid number of arguments!'
        except ValueError:
            return 'Please check if the Name or Phone were entered correctly.'
        except KeyError:
            return 'Record does not Exist.'
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
    phone = Phone(args[1])
    if not name.is_valid_name() or not phone.is_valid_phone():
        raise ValueError

    if name.value not in addressbook:
        record = Record(name, phone)
        message = addressbook.add_record(record)
    else:
        message = addressbook[name.value].add_phone(phone)
    return message


@input_error
def show_handler(addressbook: AddressBook, *args) -> str:
    message = addressbook.show_all_records()
    return message


@input_error
def change_handler(addressbook: AddressBook, *args) -> str:
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    if not old_phone.is_valid_phone() and not new_phone.is_valid_phone():
        raise ValueError
    message = addressbook.data[args[0]].change_phone(old_phone, new_phone)
    return message


@input_error
def del_handler(addressbook: AddressBook, *args):
    if args[0] == 'phone':
        phone = Phone(args[2])
        addressbook[args[1]].delete_phone(phone)
        message = 'Phone was deleted from this record'
    elif args[0] == 'record':
        message = addressbook.del_record(args[1])
    else:
        message = f'del command does not support {args[0]} argument'
    return message


function = {'hello': welcome_message,
            'help': help_message,
            'add': add_handler,
            'show': show_handler,
            'change': change_handler,
            'del': del_handler}
