from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def is_valid_name(self):
        return True if self.value.isalpha() else False


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def is_valid_phone(self):
        is_valid = True if self.value.isnumeric() else False
        return is_valid


class Record:
    def __init__(self, name: Name, phone: Phone):
        self.name = name
        self.phones = set()
        self.birthday = None
        self.phones.add(phone)

    def add_phone(self, phone) -> str:
        message = "Phone was added."
        self.phones.add(phone)
        return message

    def change_phone(self, phone: Phone, new_phone: Phone) -> str:
        message = 'Phone was not found in this record.'
        for i in self.phones:
            if i.value == phone.value:
                self.phones.remove(i)
                self.phones.add(new_phone)
                message = 'Phone has been changed.'
                break
        return message

    def delete_phone(self, phone: Phone) -> str:
        message = 'Phone was not removed because it was not found.'
        for i in self.phones:
            if i.value == phone.value:
                self.phones.remove(i)
                message = "phone deleted"
                break
        return message


class AddressBook(UserDict):
    def add_record(self, record) -> str:
        self.data[record.name.value] = record
        message = 'Record added into address book!'
        return message

    def del_record(self, name) -> str:
        self.data.pop(name)
        message = 'Record deleted from address book.'
        return message

    def show_all_records(self) -> str:
        message = f'\nRecords in address book:\n'
        for rec_id, record in self.data.items():
            message += f'{record.name.value}: {", ".join([phone.value for phone in record.phones])}\n'
        return message
