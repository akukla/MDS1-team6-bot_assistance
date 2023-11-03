from typing import Optional
from datetime import date, timedelta
from models.base_class import BaseClass
from models.demo_users import demo_users

from utils.exceptions import IncorrectFormatException
from utils.parsers import *


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value: Optional[str] = None):
        self.date: datetime = birthday_parse_or_throw(value) if value else None

    def __str__(self):
        if not self.date:
            return "No date"
        return self.date.strftime("%d.%m.%Y")


class Address(Field):
    pass


class Name(Field):
    pass


class Email(Field):
    pass


class Phone(Field):

    def __init__(self, value):
        super().__init__(phone_parse_or_throw(value))

    @staticmethod
    def is_valid(phone: str) -> bool:
        return isinstance(phone, str) and phone.isdigit() and len(phone) == 10


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phone: Optional[Phone] = None
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_address(self, address: str) -> bool:
        try:
            address_obj = Address(address)
        except IncorrectFormatException:
            print("Incorrect address format")
            return False
        self.address = address_obj
        return True

    def add_email(self, email: str) -> bool:
        try:
            email_obj = Email(email)
        except IncorrectFormatException:
            print("Incorrect email format")
            return False
        self.email = email_obj
        return True

    def add_birthday(self, birthday: str) -> bool:
        try:
            birthday_obj = Birthday(birthday)
        except IncorrectFormatException:
            print("Incorrect birthday format")
            return False
        self.birthday = birthday_obj
        return True

    def _add_birthday_datetime(self, birthday: datetime) -> bool:
        if birthday is None:
            return False
        birthday_record = Birthday()
        birthday_record.date = birthday
        self.birthday = birthday_record
        return True

    def add_phone(self, phone: str) -> bool:
        try:
            phone_obj = Phone(phone)
        except IncorrectFormatException as ex:
            print(str(ex))
            return False
        self.phone = phone_obj
        return True

    def edit_phone(self, new_phone: str) -> bool:
        try:
            phone_obj = Phone(new_phone)
        except IncorrectFormatException as ex:
            print(str(ex))
            return False
        self.phone = phone_obj
        return True

    def __str__(self):
        ret = f"Contact name: {self.name.value}, phone: {self.phone}"
        if self.birthday is not None:
            ret += f", birthday: {self.birthday}"
        if self.email is not None:
            ret += f", email: {self.email}"
        if self.address is not None:
            ret += f", address: {self.address}"
        return ret


class AddressBook(BaseClass):

    _filename: str = 'address_book.pcl'

    def add_contact(self, name: str, phone: Optional[str] = None, email: Optional[str] = None, address: Optional[str] = None, birthday: Optional[str] = None) -> bool:
        record = Record(name)
        if phone is not None:
            record.add_phone(phone)
        if email is not None:
            record.add_email(email)  # Not validating because it was validated in prompt
        if address is not None:
            record.add_address(address)
        if birthday is not None:
            record.add_birthday(birthday)
        ret = self.add_record(record)
        if ret:
            self.save()
        return ret

    def add_record(self, record: Record) -> bool:
        self.data[record.name.value] = record
        self.save()
        return True

    def find_full_match(self, name: str) -> Optional[Record]:
        if name in self.data.keys():
            return self.data[name]
        return None

    def find(self, term: str) -> Optional[list[Record]]:
        ret = []
        for key in self.data.keys():
            if key.lower().find(term.lower()) != -1:
                ret.append(self.data[key])
        return ret

    def find_by(self, field: str, value: str) -> Optional[list[Record]]:
        if field == "name":
            return self.find(value)

        ret = []
        for _, v in self.data.items():
            if field == "name" and value == v.name.value:
                ret.append(v)
            elif field == "phone" and v.phone is not None and v.phone.value.find(value) != -1:
                ret.append(v)
            elif field == "birthday" and v.birthday is not None and str(v.birthday).find(value) != -1:
                ret.append(v)
            elif field == "email" and v.email is not None and v.email.value.find(value) != -1:
                ret.append(v)
            elif field == "address" and v.address is not None and v.address.value.find(value) != -1:
                ret.append(v)

        return ret

    def enumerate(self) -> Optional[Record]:
        for item in self.data:
            # print(type(item), item)
            yield self.data[item]

    def __len__(self) -> int:
        return len(self.data)

    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            self.save()
            return True
        return False

    def _load_demo_data(self):

        for user in demo_users:
            record = Record(user['name'])
            record._add_birthday_datetime(user['birthday'])
            self.add_record(record)

    def get_birthdays(self, delta_days: int) -> list[Record]:
        ret = []
        required_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=10)
        for key in self.data:
            user: Record = self.data[key]
            if user.birthday is None or user.birthday.date is None:
                continue
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            contact_date = user.birthday.date.replace(year=datetime.today().year) if user.birthday.date.replace(year=datetime.today().year) > today else user.birthday.date.replace(year=datetime.today().year + 1)
            delta = (contact_date - today).days
            if delta == delta_days:
                ret.append(user)
        return ret
