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

from models.notes import Notes, Note

GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Cancel</highlighted-text>]: "
GIVE_ME_TEMPLATE_EMPTY_FOR_SKIP = "Give me <highlighted-text>{entity}</highlighted-text> [<highlighted-text>Empty</highlighted-text> for <highlighted-text>Skip</highlighted-text>]: "
DELETE_CONFIRMATION_NOTE = "Are you sure. Note will be <highlighted-text>Deleted</highlighted-text> [<highlighted-text>y</highlighted-text>/<highlighted-text>n</highlighted-text>, dafault:<highlighted-text>n</highlighted-text>]: "


def flow_note_add(notes: Notes) -> str:
    title_value = prompt(HTML(
            GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Note title")
        ), style=style, validator=CheckIfNoteDoesntExistValidator(notes))
    if len(title_value.strip()) == 0:
        return 'Canceled'
    
    text_value = prompt("Give me Note Text. Add # before a word if you want to make it a tag: (ESCAPE followed by ENTER to accept)\n > ", multiline=True)
    if len(text_value.strip()) == 0:
        text_value = None

    return "Note added" if notes.add(title=title_value, text=text_value) != None else "Note was not added"

def flow_note_show(note) -> str:
    # TODO: format note
    return str(note)

def flow_note_find(notes: Notes, term: str) -> str:
    # TODO: format note
    return '\n-----\n'.join([str(note) for note in notes.find_notes(term)])

def flow_note_remove(notes: Notes, note: Note) -> str:
    confirmation = prompt(HTML(
            DELETE_CONFIRMATION_NOTE
        ), style=style, validator=YesNoValidator())

    if confirmation == 'y':
        if notes.remove_note(note):
            return "Note removed"
        else:
            return "Note was not removed"
    else:
        return "Canceled"
    
def flow_note_edit(notes: Notes, note: Note) -> str:
    template = "Would you like to edit Note {field}? [<highlighted-text>y</highlighted-text>/<highlighted-text>n</highlighted-text>, dafault:<highlighted-text>n</highlighted-text>]: "
    res = False

    # Title update
    confirmation = prompt(HTML(
        template.format(field='title')
    ), style=style, validator=YesNoValidator())

    if confirmation == 'y':
        title_value = prompt(HTML(GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(entity="Note title")), style=style, validator=CheckIfNoteDoesntExistValidator(notes))
        note.title = title_value
        res = True

    # Text update
    confirmation = prompt(HTML(
        template.format(field='note text')
    ), style=style, validator=YesNoValidator())

    if confirmation == 'y':
        text_value = prompt("Give me Note Text. Add # before a word if you want to make it a tag: (ESCAPE followed by ENTER to accept)\n > ", multiline=True, default=note.text)
        if len(text_value.strip()) == 0:
            text_value = None

        note.text = text_value
        res = True
    
    return "Note updated" if res else "Note was not updated"

def flow_note_all(notes: Notes) -> str:
    # TODO: format note
    return '\n-----\n'.join([str(note) for note in notes.all_notes()])
