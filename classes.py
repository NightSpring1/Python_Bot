import re
import pickle
from datetime import date
from collections import UserDict


class Name:
    def __init__(self, name: str):
        self._name = None
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if len(value) in range(2, 16) and value.isalpha():
            self._name = value.capitalize()
        else:
            raise ValueError('Name must contain only letters and be between 2 and 15 characters long')

    def __str__(self):
        return self._name


class Phone:
    def __init__(self, number: str):
        self._number = None
        self.number = number

    @property
    def number(self) -> str:
        return self._number

    @number.setter
    def number(self, value: str):
        digits = ''.join(re.findall(r'\d', value))
        if len(digits) >= 9:
            self._number = '+380' + digits[-9:]
        else:
            raise ValueError('Phone number must have at least 9 digits')

    def __eq__(self, other: object) -> bool:
        return self.number == other.number

    def __str__(self):
        return self._number


class Birthday:
    def __init__(self, date_str: str):
        self._date = None
        self.date_str = date_str

    @property
    def date_str(self) -> str:
        return self._date.strftime("%d-%m-%Y")

    @date_str.setter
    def date_str(self, value: str):
        day, month, year = map(int, re.split(r"[-|_|\\|/]", value))
        birthday = date(year, month, day)
        if birthday >= date.today():
            raise ValueError(f'Birthday must be in the past')
        self._date = birthday

    @property
    def date(self) -> date:
        return self._date

    def __repr__(self) -> str:
        return self.date_str


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.add_phone(phone)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: Name):
        self.__name = name

    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def phones(self, phones):
        self.__phones = phones

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self.__birthday = birthday

    def add_phone(self, phone: Phone):
        if phone not in self.phones:
            self.phones.append(phone)
        else:
            raise ValueError(f"Phone {phone} already exists in {self.name} record")

    def del_phone(self, phone: Phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise KeyError(f"Phone {phone} does not exist in {self.name} record")

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        try:
            bday_this_year = self.birthday.date.replace(year=today.year)
        except ValueError:
            bday_this_year = self.birthday.date.replace(year=today.year, day=today.day - 1)
        if bday_this_year < today:
            bday_this_year = self.birthday.date.replace(year=today.year + 1)

        days_to_birthday = (bday_this_year - today).days
        return days_to_birthday


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.name] = record

    def del_record(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            raise KeyError(f'Record with name {name} does not exist')

    def show_records(self, records_per_page: int = 1, search_pattern: str = '') -> str:
        output = []
        record_count = 0
        for record in self.data.values():
            # Creates strings for each field
            name = record.name
            phones_output = ", ".join(list(map(str, record.phones)))
            birthday_output = record.birthday.date_str if record.birthday else "-"
            days_to_birthday = record.days_to_birthday() if record.birthday else ""
            # Makes final string
            search_string = f'{record_count+1}) {name}, {phones_output}, {birthday_output} {days_to_birthday}\n'
            # Searching if there are any matches according to search pattern
            if search_pattern != '':
                if re.search(search_pattern, search_string, flags=re.IGNORECASE):
                    output.append(search_string)
                    record_count += 1
            else:
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
