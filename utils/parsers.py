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

