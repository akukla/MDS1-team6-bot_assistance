from datetime import datetime
import re
from utils.exceptions import IncorrectFormatException


def birthday_parse_or_throw(value) -> datetime:
    """
    Create birthday date if it has a valid format (DD.MM.YYYY).

    Returns:
    - datetime if the birthday date has a valid format, raise Exception otherwise.

    Raises:
        IncorrectFormatException: date has incorrect format
    """
    pattern = '^(\d{2})\.(\d{2})\.(\d{4})$'
    match_result = re.match(pattern, value)
    if match_result is None:
        raise IncorrectFormatException("Incorrect birthday format. Valid format is DD.MM.YYYY")

    try:
        return datetime.strptime(value, '%d.%m.%Y')
    except ValueError:
        raise IncorrectFormatException("Incorrect birthday format. Provided string is not valid date")

def phone_parse_or_throw(phone: str) -> str:
    """
    Validate and return phone number if it has valid format

    Returns:
    - phone number, raise Exception otherwise.

    Raises:
        IncorrectFormatException: date has incorrect format
    """
    if isinstance(phone, str) and phone.isdigit() and len(phone) == 10:
        return phone
    raise IncorrectFormatException("Incorrect phone format. Phone must contain 10 digits")


# bot functions_errors
from utils.decorators import input_error

@input_error

def add_birthday(args, book):
    if len(args) != 2:
        return "Please provide a name and a birthday."
    name, birthday = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    if record.birthday:
        response = input(f"{name} already has a birthday on {record.birthday.value.strftime('%d.%m.%Y')}. Would you like to change it? (yes/no): ")
        if response.lower() != 'yes':
            return "Birthday was not changed."
        record.edit_birthday(birthday)
        return f"{name}'s birthday updated to {birthday}."
    
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    if not record.birthday:
        return "No birthday set for this contact."
    return f"{record.name.value}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."

@input_error
def upcoming_birthdays(book, n):
    birthdays = book.get_birthdays_for_week()
    if not birthdays:
        return "No birthdays in the upcoming week."
    else:
        result = []
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days_order:
            if day in birthdays:
                result.append(f"{day}: {', '.join(birthdays[day])}")
        return "\n".join(result)
@input_error

def show_all(book):
    records = book.all_records()
    if not records:
        return "No contacts found."
    return "\n".join(str(record) for record in records)
