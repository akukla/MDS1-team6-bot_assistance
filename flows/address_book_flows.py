from models.address_book import AddressBook
from models.notes import Notes
from actions import *
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter, DummyCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.formatted_text import ANSI, HTML
from flows.styles import style
from flows.validators import *


GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Cancel</highlighted-text>]: "
GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Skip</highlighted-text>]: "

def flow_contact_add(book: AddressBook) -> str:
    contact_name = prompt(HTML(
            GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Contact Name")
        ), style=style, validator=CheckForContactExistValidator(book))
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