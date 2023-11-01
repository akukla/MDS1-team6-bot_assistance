from utils.decorators import input_error
from models.address_book import AddressBook, Record


@input_error("Give me name and phone please")
def add_contact(args, book: AddressBook):
    name, phone = args
    record = Record(name)
    if not record.add_phone(phone):
        return "Contact not added"
    book.add_record(record)
    return "Contact added."


@input_error("Give me name and phone please")
def change_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        return "Contact not found"
    if not record.edit_phone(phone):
        return "Contact not updated."
    return "Contact updated."


@input_error("Enter user name")
def get_contact(args, book: AddressBook):
    name, = args
    contact = book.find(name)

    if not contact:
        return "Contact not found"
    return contact.phone.value


def get_all_contacts(book: AddressBook):
    # TODO: Update 
    if len(book) == 0:
        return 'Address book is empty'
    ret = []
    for item in book.enumerate():
        ret.append(str(item))
    return '\n'.join(ret)


def print_birthdays(args, book):
    birthdays = book.get_birthdays_per_week()
    if len(birthdays):
        return str('\n'.join(birthdays))
    else:
        return 'You don\'t have any birthdays next week'


@input_error("Incorect parameters. Correct format parameters is: add-birthday name birthday")
def add_birthday(args, book: AddressBook):
    name, bithday = args
    record = book.find(name)
    if record is None:
        return 'Contact not found'
    
    if not record.add_birthday(bithday):
        return "Birthday not added"

    return 'Birthday added'


@input_error("Incorect parameters. Correct format parameters is: show-birthday name")
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record is None:
        return 'Contact not found'
    
    if record.birthday is None:
        return 'Birthday is not defined'

    return str(record.birthday)