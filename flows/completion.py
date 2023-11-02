from typing import Optional
from prompt_toolkit.completion import NestedCompleter, DummyCompleter, Completer, Completion
from models.address_book import AddressBook
from models.notes import Notes

class SelectUserCompleter(Completer):

    def __init__(self, book: AddressBook, quote=True) -> None:
        self.quote = quote
        self.book = book
        super().__init__()

    def get_completions(self, document, complete_event):
        term = document.text
        for item in  self.book.find(term):
            yield Completion(f'"{item.name.value}"') if self.quote else Completion(item.name.value)


class SelectNoteCompleter(Completer):

    def __init__(self, notes: Notes, quote=True) -> None:
        self.quote = quote
        self.notes = notes
        super().__init__()

    def get_completions(self, document, complete_event):
        term = document.text
        for item in  self.notes.find_note(term):
            yield Completion(f'"{item.name.value}"') if self.quote else Completion(item.name.value)


# Notes

class FindNotesCompleter(Completer):

    def __init__(self, notes: Notes, quote=True) -> None:
        self.quote = quote
        self.notes = notes
        super().__init__()

    def get_completions(self, document, complete_event):
        term = document.text.strip()
        for item in self.notes.find_notes(term):
            yield Completion(f'"{item.title}"') if self.quote else Completion(item.title)

class TagsCompleter(Completer):
    def __init__(self, notes:Notes) -> None:
        self.notes = notes
        super().__init__()

    def get_completions(self, document, complete_event):
        term = document.text.strip()
        for item in self.notes.collect_tags():
            if term in item:
                yield Completion(f'{item}')