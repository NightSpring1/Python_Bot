import re
from collections import UserDict


class Name:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value.isalpha() and len(value) in range(2, 16):
            self.__value = value.capitalize()
        else:
            raise ValueError  # invalid name


class Phone:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if len(value) >= 9:
            value = '+380' + ''.join(re.findall(r"[0-9]", value))[-9:]
            self.__value = value
        else:
            raise ValueError  # phone has not enough digits


class Record:
    def __init__(self, name: Name, phone: Phone = None):
        self.__name = name
        self.__phones = set()
        self.phones = phone
        self.birthday = None

    @property
    def name(self):
        return self.__name

    @property
    def phones(self):
        return set(map(lambda x: x.value, self.__phones))

    @phones.setter
    def phones(self, phone: Phone):
        if phone is None:
            pass
        elif phone.value not in self.phones:
            self.__phones.add(phone)
        else:
            raise ValueError  # phone already exists

    def add_phone(self, phone: Phone):
        self.phones = phone

    def del_phone(self, key: Phone):
        if key.value in self.phones:
            for phone in self.__phones:
                if phone.value == key.value:
                    self.__phones.remove(phone)
                    break
        else:
            raise KeyError  # phone does not exist


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def del_record(self, name):
        self.data.pop(name)

    def show_records(self) -> str:
        records = []
        for record in self.data.values():
            records.append(f'{record.name.value}:\t{", ".join(record.phones)}.')
        return '\n'.join(records)
