from handlers import function
from classes import AddressBook


def main() -> None:
    print('Type "help" for list of commands.')
    my_address_book = AddressBook()
    while True:
        input_string = input('Enter Command: ').strip().lstrip()
        command = input_string.split()[0].lower()
        arguments = input_string.split()[1:]

        if command in function:
            message = function[command](my_address_book, *arguments)

        elif input_string.lower() in ('good bye', 'exit', 'close'):
            message = 'Good bye!'

        else:
            message = f'Command {command} does not exist!'

        print(message)

        if message == 'Good bye!':
            break


if __name__ == '__main__':
    main()
