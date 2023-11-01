import shlex
from typing import Optional
from flows.completion import SelectUserCompleter
from models.address_book import AddressBook
from models.notes import Notes
from prompt_toolkit.completion import NestedCompleter, DummyCompleter, Completer, Completion
from flows.validators import *


def parse_input(user_input) -> tuple[str, Optional[str], Optional[list]]:
    input_list = shlex.split(user_input)
    if len(input_list) == 0:
        return (None, None, None)
    elif len(input_list) == 1:
        return (None, input_list[0].strip().lower(), None)
    elif len(input_list) == 2:
        module, cmd = input_list
        cmd = cmd.strip().lower()
        module = module.strip().lower()
        return (module, cmd, None)
    else:
        module, cmd, *args = input_list
        cmd = cmd.strip().lower()
        module = module.strip().lower()
        return (module, cmd, *args)


def get_main_completion(book: AddressBook, notes: Notes) -> Completer:
    return NestedCompleter.from_nested_dict({
        'contacts': {
            'add': None,
            'all': None,
            'edit': SelectUserCompleter(book=book),
            'delete': SelectUserCompleter(book=book),
        },
        
        'exit': None,
        'close': None,
        'quit': None
    })

                # 'phone': DummyCompleter(validator=PhoneValidator()),
                # 'email': DummyCompleter(validator=EmailValidator()),
                # 'address': DummyCompleter(),
                # 'birthday': DummyCompleter(validator=DateValidator()),