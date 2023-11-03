"""
This module contains functions for handling contact-related flows in the assistant bot.
"""

from typing import Optional

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML

from models.address_book import AddressBook

from actions import *

from flows.styles import style
from flows.validators import *
from flows.completion import SelectUserCompleter


GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Cancel</highlighted-text>]: "
GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Skip</highlighted-text>]: "
DELETE_CONFIRMATION_CONTACT = "Are you sure? Contact <highlighted-text>{entity}</highlighted-text> will be <highlighted-text>Deleted</highlighted-text> [<highlighted-text>y</highlighted-text>/<highlighted-text>n</highlighted-text>, default: <highlighted-text>n</highlighted-text>]: "


def flow_contact_add(book: AddressBook) -> str:
    """
    Adds a contact to the address book.

    Args:
        book (AddressBook): The address book to add the contact to.

    Returns:
        str: A message indicating whether the contact was added or not.
    """
    contact_name = prompt(HTML(
        GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Contact Name")
    ), style=style, validator=CheckIfContactDoesntExistValidator(book))
    if len(contact_name.strip()) == 0:
        return 'Canceled'

    contact_phone = prompt(HTML(
        GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP.format(entity="Contact Phone")
    ), style=style, validator=PhoneValidator())
    if len(contact_phone.strip()) == 0:
        contact_phone = None

    contact_email = prompt(HTML(
        GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP.format(entity="Contact Email")
    ), style=style, validator=EmailValidator())
    if len(contact_email.strip()) == 0:
        contact_email = None

    contact_address = prompt(HTML(
        GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP.format(entity="Contact Address")
    ), style=style)
    if len(contact_address.strip()) == 0:
        contact_address = None

    contact_birthday = prompt(HTML(
        GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP.format(entity="Contact Birthday")
    ), style=style, validator=DateValidator())
    if len(contact_birthday.strip()) == 0:
        contact_birthday = None

    return "Contact added" if book.add_contact(contact_name, phone=contact_phone, email=contact_email, address=contact_address, birthday=contact_birthday) == True else "Contact was not added"


def flow_contact_edit(book: AddressBook, args: list[str]) -> str:
    """
    Edits a contact in the address book.

    Args:
        book (AddressBook): The address book to edit the contact in.
        args (list): List of arguments for the contact edit.

    Returns:
        str: A message indicating the result of the contact edit.
    """
    contact_name: Optional[str] = None

    if len(args) > 0 and args[0] is not None and book.find_full_match(args[0]) is not None:
        contact_name = args[0]
    else:
        contact_name = prompt(HTML(
            GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Contact Name")
        ), style=style, validator=CheckIfContactDoesntExistValidator(book), completer=SelectUserCompleter(book), complete_while_typing=True)
    if len(contact_name.strip()) == 0:
        return 'Canceled'

    record = book.find_full_match(contact_name)

    available_fields = ["phone", "email", "address", "birthday",]
    field_completion = WordCompleter(available_fields, ignore_case=True,)

    field = prompt(
        HTML(
            f"What field would you like to edit? <highlighted-text>{str(available_fields)}</highlighted-text> or <highlighted-text>Leave Empty for Skip</highlighted-text>: "),
        style=style,
        completer=field_completion,
        validator=SimpleListValidator(available_fields, allow_empty=True)
    ).strip()
    if len(field.strip()) == 0:
        return 'Canceled'

    if field == 'phone':
        value_for_editing = prompt(
            HTML(
                f"What is your <highlighted-text>new phone</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
            style=style,
            validator=PhoneValidator()
        ).strip()

        if len(value_for_editing) == 0:
            record.phone = None
            return 'Phone was deleted'
        record.edit_phone(value_for_editing)
        return "Phone was changed"
    elif field == 'email':
        value_for_editing = prompt(
            HTML(
                f"What is your <highlighted-text>new email</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
            style=style,
            validator=EmailValidator()
        ).strip()

        if len(value_for_editing) == 0:
            record.email = None
            return 'Email was deleted'
        record.add_email(value_for_editing)
        return "Email was changed"
    elif field == 'birthday':
        value_for_editing = prompt(
            HTML(
                f"What is your <highlighted-text>new birthday</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
            style=style,
            validator=DateValidator()
        ).strip()

        if len(value_for_editing) == 0:
            record.birthday = None
            return 'Delete birthday'
        record.add_birthday(value_for_editing)
        return "Birthday was changed"
    elif field == 'address':
        value_for_editing = prompt(
            HTML(
                f"What is your <highlighted-text>new address</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
            style=style,
        ).strip()

        if len(value_for_editing) == 0:
            record.address = None
            return 'Delete address'
        record.address = value_for_editing
        return "Address was changed"

    # It is impossible to reach this line if validators work fine
    return None


def flow_contact_remove(book: AddressBook, record: Record) -> str:
    """
    Removes a contact from the address book.

    Args:
        book (AddressBook): The address book to remove the contact from.
        record (Record): The contact record to be removed.

    Returns:
        str: A message indicating the result of the contact removal.
    """
    confirmation = prompt(HTML(
        DELETE_CONFIRMATION_CONTACT.format(entity=record.name.value)
    ), style=style, validator=YesNoValidator())

    if confirmation == 'y':
        book.delete(record.name.value)
        return "Contact removed"

    return "Canceled"


def flow_contact_find(book: AddressBook) -> str:
    """
    Finds contacts in the address book based on a search field and value.

    Args:
        book (AddressBook): The address book to search in.

    Returns:
        str: A formatted table displaying the search results.
    """
    available_fields = ["name", "phone", "email", "address", "birthday"]
    field_completion = WordCompleter(available_fields, ignore_case=True)

    while True:
        field = prompt(
            HTML(
                f"What field for search would you like to use? <highlighted-text>{str(available_fields)}</highlighted-text> or <highlighted-text>Leave Empty</highlighted-text> to cancel search: "),
            style=style,
            completer=field_completion,
            validator=SimpleListValidator(available_fields, allow_empty=True)
        ).strip()

        if len(field.strip()) == 0:
            return 'Canceled'

        field_value = prompt(HTML(
            GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Field value")
        ), style=style, validator=None)

        if len(field_value.strip()) != 0:
            break

    columns_width = [30, 12, 30, 40, 10]
    row_delimiter = "| " + " | ".join(
        f"{'-' * t:^{t}}" for t in columns_width) + " |"

    table = row_delimiter
    table += "\n"

    table += "| " + " | ".join(
        f"{t[0]:^{t[1]}}" for t in zip(available_fields, columns_width)) + " |"
    table += "\n"

    table += row_delimiter
    table += "\n"

    for record in book.find_by(field, field_value):
        row_data = [record.name.value]

        if record.phone:
            row_data.append(record.phone.value)
        else:
            row_data.append("")

        if record.email:
            row_data.append(record.email)
        else:
            row_data.append("")

        if record.address:
            row_data.append(record.address)
        else:
            row_data.append("")

        if record.birthday:
            row_data.append(str(record.birthday))
        else:
            row_data.append("")

        table_row = "| " + " | ".join(
            f"{t[0]:^{t[1]}}" for t in zip(row_data, columns_width)) + " |"
        table += table_row
        table += "\n"

        table += row_delimiter
        table += "\n"

    return table


def flow_contact_birthdays(book: AddressBook, args: list[str]) -> str:
    delta_days = 0
    if len(args) > 0 and args[0] is not None:
        try:
            DateDeltaValidator.validate_text(args[0])
            delta_days = int(args[0])
        except ValidationError:
            pass
            # return DateDeltaValidator.message

    if delta_days == 0:
        while True:
            str_value = prompt(
                HTML(
                    f"How many <highlighted-text>days</highlighted-text> should i add from today to shouw birthdays? [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Cancel</highlighted-text>]: "),
                style=style,
                validator=DateDeltaValidator()
            ).strip()

            if len(str_value) == 0:
                return 'Canceled'
            else:
                try:
                    DateDeltaValidator.validate_text(str_value)
                    delta_days = int(str_value)
                    break
                except ValidationError:
                    print(
                        "Provide valid days count. Valid command format is: contacts birthdays DAYS")

    records = book.get_birthdays(delta_days)
    return "\n-----\n".join([str(record) for record in records])
