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



def flow_note_find(notes: Notes, term: str) -> str:
    delimeter_str = "\n" + "*" * 80 + "\n"
    notes_str = delimeter_str

    filtered_notes = notes.find_notes(term)

    if len(filtered_notes) == 0:
        return "No notes found."

    for note in filtered_notes:
        notes_str += "\n" + note.title + "\n"
        notes_str += "-" * len(note.title) + "\n\n"
        notes_str += note.text if note.text else ""
        notes_str += delimeter_str

    return notes_str


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
        title_value = prompt(HTML(GIVE_ME_TEMPLATE_EMPTY_FOR_CANCEL.format(
            entity="Note title")), style=style, validator=CheckIfNoteDoesntExistValidator(notes))
        note.title = title_value
        res = True

    # Text update
    confirmation = prompt(HTML(
        template.format(field='note text')
    ), style=style, validator=YesNoValidator())

    if confirmation == 'y':
        text_value = prompt(
            "Give me Note Text. Add # before a word if you want to make it a tag: (ESCAPE followed by ENTER to accept)\n > ", multiline=True, default=note.text)
        if len(text_value.strip()) == 0:
            text_value = None

        note.text = text_value
        notes.update_tags()
        res = True

    return "Note updated" if res else "Note was not updated"


def flow_note_all(notes: Notes) -> str:
    delimeter_str = "\n" + "*" * 80 + "\n"
    notes_str = delimeter_str

    notes_to_print = notes.all_notes()

    if len(notes_to_print) == 0:
        return "No notes to print."

    for note in notes_to_print:
        notes_str += "\n" + note.title + "\n"
        notes_str += "-" * len(note.title) + "\n\n"
        notes_str += note.text if note.text else ""
        notes_str += delimeter_str

    return notes_str


def flow_tags_find_tag(notes: Notes, args: list[Optional[str]]) -> str:
    query: Optional[str] = args[0] if len(args) > 0 else None

    if query == None:
        query = prompt("Give me Tag Name: ", style=style, completer=WordCompleter(
            notes.collect_tags(), ignore_case=True,))

    delimeter_str = "\n" + "*" * 80 + "\n"
    result_str = delimeter_str

    filtered_notes = notes.find_tag(query)

    if len(filtered_notes) == 0:
        return "No notes found."

    for tag, titles in filtered_notes.items():
        result_str += "\n" + f"{'Tag: ':<10}" + tag + "\n"
        result_str += f"{'Titles: ':<10}"
        result_str += ', '.join([title for title in titles]) + "\n"
        result_str += delimeter_str

    return result_str



def flow_tags_all_tags(notes: Notes) -> str:
    return ', '.join(["#" + str(tag) for tag in notes.all_tags()])
    


def flow_tags_all_tags_revert(notes: Notes) -> str:
    return ', '.join(["#" + str(tag) for tag in notes.all_tags_revert()])



def flow_tags_alpsort_tags(notes: Notes) -> str:
    return ', '.join(["#" + str(tag) for tag in notes.alpsort_tags()])



def flow_tags_alpsort_tags_revert(notes: Notes) -> str:
    return ', '.join(["#" + str(tag) for tag in notes.all_tags_revert()])



def flow_notes_find_by_tag(notes, tag: Optional[str]) -> str:
    if tag is None:
        tag = prompt("Give me Tag Name [Empty for Cancel]: ", style=style, completer=WordCompleter(notes.collect_tags(), ignore_case=True,))
    
    if tag is None:
        return 'Canceled'

    filtered_notes = notes.find_notes_by_tag(tag)

    if len(filtered_notes) == 0:
        return "No notes found."

    delimeter_str = "\n" + "*" * 80 + "\n"
    notes_str = delimeter_str

    for note in filtered_notes:
        notes_str += "\n" + note.title + "\n"
        notes_str += "-" * len(note.title) + "\n\n"
        notes_str += note.text if note.text else ""
        notes_str += delimeter_str

    return notes_str