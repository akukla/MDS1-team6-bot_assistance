import shlex
from typing import Optional
from flows.completion import FindNotesCompleter, SelectUserCompleter, TagsCompleter
from models.address_book import AddressBook
from models.notes import Notes
from prompt_toolkit.completion import NestedCompleter, DummyCompleter, Completer, Completion
from flows.validators import *


def parse_input(user_input) -> tuple[str, Optional[str], Optional[list]]:
    try:
        user_input = user_input.strip()
        input_list = shlex.split(user_input)
    except ValueError:
        return (None, None, None)

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
            'remove': SelectUserCompleter(book=book),
            'find': None,
            'birthdays': None,
        },
        "notes": {
            'add': None,
            'all': None,
            'find': FindNotesCompleter(notes=notes),
            'find_by_tag': TagsCompleter(notes=notes),
            'remove': FindNotesCompleter(notes=notes),
            'edit': FindNotesCompleter(notes=notes),
        },

        "tags": {
            'find_tag': TagsCompleter(notes=notes),
            'all_tags': None,
            'all_tags_revert ': None,
            'alpsort_tags': None,
            'alpsort_tags_revert': None,
        },

        'help': None,
        'exit': None,
        'close': None,
        'quit': None
    })


help_text = """
This is a simple assistant bot. It can help you to manage your contacts and notes. 

Autocoplete is available for all commands. To use autocomplete just press arrow keys and space to confirm.

Commands examples:
    contacts all - show all contacts
    contacts edit "Jhon Doe" - add new contact
    notes all - show all notes
    notes remove "Note Title" - remove note by title

Commands:
        contacts
            add - add new contact
            all - show all contacts
            edit "CONTACT_NAME" - edit contact
            remove "CONTACT_NAME" - remove contact
            find - find contact
            birthdays "DAYS" - show contacts birthdays in "DAYS" days

        notes
            add - add new note
            all - show all notes
            find "NOTE_TITLE" - find note by title
            find_by_tag "TAG" - find notes by tag
            remove "NOTE_TITLE" - remove note by title
            edit "NOTE_TITLE" - edit note by title

        tags
            find_tag - find tag and show all note title with this tag
            all_tags - show all tags by usage
            all_tags_revert - show all tags by usage in reverse order
            alpsort_tags - show all tags alphabetically
            alpsort_tags_revert - show all tags alphabetically in reverse order
        
        help - show this help
        exit or close or quit - close application
"""
