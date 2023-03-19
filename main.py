STORAGE = {'diana': '380509876523',
           'alex': '380638790931',
           'noname': '380928742311'}


def input_error(func):
    def execute(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Please enter valid arguments!'
        except ValueError:
            return 'Please check if the Name and Phone were entered correctly.'
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
    add "user name" "user phone" : adds contact to the storage
    change "user name" "new phone": change existing number to a new one
    show all: shows all contacts
    show phone "phone": shows user of specified phone
    show name "name": show phone of specified user
    '''

    return message


@input_error
def add_record(*args) -> str:
    if args[0] in STORAGE:
        message = 'This contact already exists.'

    elif not args[0].isalpha() or not args[1].isnumeric():
        message = 'Name or phone were entered incorrectly.'

    else:
        STORAGE[args[0]] = args[1]
        message = 'Record added Successfully.'

    return message


@input_error
def get_record(*args) -> str:
    if args[0].lower() == 'all':
        message = ''
        for name, phone in STORAGE.items():
            message += f'{name}: {phone}\n'
        message = message.strip()

    elif args[0].lower() == 'name':
        message = f'Phone of {args[1]} is {STORAGE[args[1]]}'

    elif args[0].lower() == 'phone':
        message = f'Phone not found.'
        for name, phone in STORAGE.items():
            if phone == args[1]:
                message = f'User of {phone} phone is {name}'

    else:
        message = f'show command does not support argument "{args[0]}".'

    return message


@input_error
def change_record(*args) -> str:
    if not args[1].isnumeric():
        message = 'Please enter valid phone number.'

    elif args[0] not in STORAGE:
        message = 'Contact was not found.'

    else:
        STORAGE[args[0]] = args[1]
        message = 'Contact changed Successfully.'

    return message


function = {'hello': welcome_message,
            'add': add_record,
            'show': get_record,
            'change': change_record,
            'help': help_message}


def main() -> None:
    print('Type "help" for list of commands.')

    while True:
        input_string = input('Enter Command: ').strip().lstrip()
        command = input_string.split()[0].lower()
        arguments = input_string.split()[1:]

        if command in function:
            message = function[command](*arguments)

        elif input_string.lower() in ('good bye', 'exit', 'close'):
            message = 'Good bye!'

        else:
            message = f'Command {command} does not exist!'

        print(message)

        if message == 'Good bye!':
            break


if __name__ == '__main__':
    main()
