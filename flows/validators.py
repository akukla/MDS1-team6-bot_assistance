
from prompt_toolkit.validation import Validator, ValidationError
from models.address_book import AddressBook
from models.notes import Notes

class YesNoValidator(Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, document):
        text = document.text.strip().lower()

        if len(text) > 0 and text not in ['y', 'n']:
            raise ValidationError(message='Please provide y or n')

class CheckIfNoteDoesntExistValidator(Validator):
    def __init__(self, notes: Notes) -> None:
        self.notes = notes
        super().__init__()

    def validate(self, document):
        text = document.text

        if len(document.text) > 0:
            if not text.isascii():
                raise ValidationError(message='Note should be in English')
            if self.notes.find_full_match(text) is not None or not text.isascii():
                raise ValidationError(message='Note with this title already exist')


class CheckIfContactDoesntExistValidator(Validator):
    def __init__(self, book: AddressBook) -> None:
        self.book = book
        super().__init__()

    def validate(self, document):
        text = document.text

        if self.book.find_full_match(text) is not None:
            raise ValidationError(message='Contact already exist')
        

class CheckIfContactExistValidator(Validator):
    def __init__(self, book: AddressBook) -> None:
        self.book = book
        super().__init__()

    def validate(self, document):
        text = document.text

        if self.book.find_full_match(text) is None:
            raise ValidationError(message='Contact already exist')
        
class SimpleListValidator(Validator):
    def __init__(self, items: list[str], allow_empty=False) -> None:
        self.items = items
        self.allow_empty = allow_empty
        super().__init__()

    def validate(self, document):
        text = document.text.strip()

        if text not in self.items and (self.allow_empty == True and len(text) == 0):
            raise ValidationError(message=f'Provided text should be one item from following list {str(self.items)}')


class PhoneValidator(Validator):

    def validate(self, document):
        text = document.text

        # TODO: Implement this method
        if len(text.strip()) > 0 and len(text.strip()) != 10:
            raise ValidationError(message='Invalid phone format. Phone should contain 10 digits.')


class EmailValidator(Validator):

    def validate(self, document):
        text = document.text

        # TODO: Implement this method


class DateValidator(Validator):

    def validate(self, document):
        text = document.text

        # TODO: Implement this method
