import re
import pickle
from datetime import date
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
            value = '+380' + ''.join(re.findall(r'[0-9]', value))[-9:]
            self.__value = value
        else:
            raise ValueError  # phone has not enough digits


class Birthday:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        b_day = re.split(r"[-|_|\\|/]", value)
        birthday_day = date(day=int(b_day[0]), month=int(b_day[1]), year=int(b_day[2]))
        if (date.today() - birthday_day).days > 0:  # birthday cannot be tomorrow
            self.__value = birthday_day
        else:
            raise ValueError


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.__name = name
        self.__phones = set()
        self.__birthday = None
        self.phones = phone
        self.birthday = birthday

    @property
    def name(self):
        return self.__name

    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def phones(self, phone: Phone):
        if phone is None:
            pass
        elif phone.value not in self.phones:
            self.__phones.add(phone)
        else:
            raise ValueError  # phone already exists

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self.__birthday = birthday

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

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday.value is None:
            days_to_birthday = None
        else:
            today = date.today()
            try:
                td_this_year = self.__birthday.value.replace(year=today.year)
                td_next_year = self.__birthday.value.replace(year=today.year + 1)
            except ValueError:  # leap year
                td_this_year = self.__birthday.value.replace(year=today.year, day=self.__birthday.value.day - 1)
                td_next_year = self.__birthday.value.replace(year=today.year + 1, day=self.__birthday.value.day - 1)
            days_to_birthday = ((td_this_year if td_this_year >= today else td_next_year) - today).days
        return days_to_birthday


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def del_record(self, name):
        self.data.pop(name)

    def show_records(self, records_per_page: int = 1, search_pattern: str = '') -> str:

        output = []
        record_count = 0
        for record in self.data.values():
            # Creates strings for each field
            name = record.name.value
            phones_output = ", ".join([phone.value for phone in record.phones])
            birthday_output = record.birthday.value.strftime("%d-%m-%Y") if record.birthday else "-"
            days_to_birthday = record.days_to_birthday() if record.birthday else ""
            # Makes  final string
            search_string = f'{record_count+1}) {name}, {phones_output}, {birthday_output} {days_to_birthday}\n'
            # Searching if there are any matches according to search pattern
            if re.search(search_pattern, search_string, flags=re.IGNORECASE):
                output.append(search_string)
                record_count += 1
            # return string with records_per_page records
            if record_count % records_per_page == 0:
                yield ''.join(output)
                output = []
        # return last page if it is not complete
        if output:
            yield ''.join(output)

    def save_records_to_file(self, filename):
        with open(filename, "wb") as fw:
            pickle.dump(self.data, fw)

    def read_records_from_file(self, filename):
        try:
            with open(filename, "rb") as fr:
                content = pickle.load(fr)
                self.data.update(content)
        except FileNotFoundError:
            pass
