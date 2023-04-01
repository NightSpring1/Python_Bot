from handlers import function
from classes import AddressBook


def command_parser(addressbook: AddressBook, input_string) -> str:
    input_string = input_string.strip().lstrip()
    command = input_string.split()[0].lower()
    arguments = input_string.split()[1:]
    if command in function:
        message = function[command](addressbook, *arguments)
    elif input_string.lower() in ('good bye', 'exit', 'close'):
        message = 'Good bye!'
    else:
        message = f'Command {command} does not exist!'
    return message


def main() -> None:
    print('Type "help" for list of commands.')
    my_address_book = AddressBook()
    while True:
        input_string = input('Enter Command: ')
        if not len(input_string):
            continue
        message = command_parser(my_address_book, input_string)
        print(message)
        if message == 'Good bye!':
            break


if __name__ == '__main__':
    main()
