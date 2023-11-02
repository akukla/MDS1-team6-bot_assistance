from typing import Optional
from flows.completion import SelectUserCompleter
from models.address_book import AddressBook
from models.notes import Notes
from actions import *
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter, DummyCompleter, WordCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.formatted_text import ANSI, HTML
from flows.styles import style
from flows.validators import *
from prompt_toolkit.shortcuts import CompleteStyle


GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Cancel</highlighted-text>]: "
GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Skip</highlighted-text>]: "
DELETE_CONFIRMATION_CONTACT = "Are you sure. Contact <highlighted-text>{entity}</highlighted-text> will be <highlighted-text>Deleted</highlighted-text> [<highlighted-text>y</highlighted-text>/<highlighted-text>n</highlighted-text>, dafault:<highlighted-text>n</highlighted-text>]: "

def flow_contact_add(book: AddressBook) -> str:
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
        GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP.format(entity="Contact email")
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

    return "Contact added" if book.add_contact(contact_name, phone=contact_phone, email=contact_email, address=contact_address) == True else "Contact was not added"

def flow_contact_edit(book: AddressBook, args: list[str]) -> str:
    contact_name: Optional[str] = None

    if len(args) > 0 and args[0] is not None and book.find_full_match(args[0]) is not None:
        contact_name = args[0]
    else:
        contact_name = prompt(HTML(
                GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Contact Name")
            ), style=style, validator=CheckIfContactDoesntExistValidator(book), completer=SelectUserCompleter(book), complete_while_typing=True)
    if len(contact_name.strip()) == 0:
        return 'Canceled'

    available_fields = ["phone", "email", "address", "birthday",]
    field_completion = WordCompleter(available_fields, ignore_case=True,)

    field = prompt(
        HTML(f"What fiald would you like to edit? <highlighted-text>{str(available_fields)}</highlighted-text> or <highlighted-text>Leave Empty for Skip</highlighted-text>: "),
        style=style,
        completer=field_completion,
        validator=SimpleListValidator(available_fields, allow_empty=True)
    ).strip()
    if len(field.strip()) == 0:
        return 'Canceled'
    
    if field == 'phone':
        value_for_editing = prompt(
                HTML(f"What is you <highlighted-text>new phone</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
                style=style,
                validator=PhoneValidator()
            ).strip()
            
        if len(value_for_editing) == 0:
            # TODO: Implement delete phone number from contact
            return 'Delete Phone'
        # TODO: implement change contact phone
        return "Phone was changed"
    elif field == 'email':
        value_for_editing = prompt(
                HTML(f"What is you <highlighted-text>new email</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
                style=style,
                validator=EmailValidator()
            ).strip()
            
        if len(value_for_editing) == 0:
            # TODO: Implement delete email from contact
            return 'Delete Email'
        # TODO: implement change email
        return "Email was changed"
    elif field == 'birthday':
        value_for_editing = prompt(
                HTML(f"What is you <highlighted-text>new birthday</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
                style=style,
                validator=DateValidator()
            ).strip()
            
        if len(value_for_editing) == 0:
            # TODO: Implement delete birthdat for contact
            return 'Delete birthday'
        # TODO: implement change email
        return "Birthday was changed"
    elif field == 'address':
        value_for_editing = prompt(
                HTML(f"What is you <highlighted-text>new address</highlighted-text> [<highlighted-text>Empty</highlighted-text> to <highlighted-text>Delete</highlighted-text>]: "),
                style=style,
            ).strip()
            
        if len(value_for_editing) == 0:
            # TODO: Implement delete birthdat for contact
            return 'Delete address'
        # TODO: implement change email
        return "Address was changed"

    # It imposible to go to this line if validators work fine
    return None

def flow_contact_remove(book: AddressBook, record: Record) -> str:
    confirmation = prompt(HTML(
        DELETE_CONFIRMATION_CONTACT.format(entity=record.name.value)
    ), style=style, validator=YesNoValidator())

    if confirmation == 'y':
        book.delete(record.name.value)
        return "Contact removed"

    return "Canceled"

def flow_contact_find(book: AddressBook, term: str) -> str:
    # TODO: Format output and show meesage if result is empty
    return '\n-----\n'.join([str(note) for note in book.find(term)])