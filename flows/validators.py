"""
Validation Module

This module provides custom validators for various input types, such as email addresses,
phone numbers, dates, and lists. These validators can be used with the prompt_toolkit library
to validate user input in an interactive application, ensuring data consistency and correctness.

Classes:
    - CheckIfContactDoesntExistValidator: Validator to check if a contact doesn't exist in
      the AddressBook.
    - CheckIfContactExistValidator: Validator to check if a contact already exists in
      the AddressBook.
    - SimpleListValidator: Validator to check if the input text is in a list of items.
    - PhoneValidator: Validator to check the format of a phone number.
    - EmailValidator: Validator to check the format of an email address.
    - DateValidator: Validator to check the format of a date in DD.MM.YYYY format.
"""

import re

from datetime import datetime
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
    """Validator to check if a contact doesn't exist in the AddressBook."""

    def __init__(self, book: AddressBook) -> None:
        """
        Initialize the validator with an AddressBook instance.

        Args:
            book (AddressBook): The AddressBook to check for contact existence.
        """
        self.book = book
        super().__init__()

    def validate(self, document):
        """Validate the input document.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the contact already exists in the AddressBook.
        """
        text = document.text

        if self.book.find_full_match(text) is not None:
            raise ValidationError(message='Contact already exists')


class CheckIfContactExistValidator(Validator):
    """Validator to check if a contact already exists in the AddressBook."""

    def __init__(self, book: AddressBook) -> None:
        """
        Initialize the validator with an AddressBook instance.

        Args:
            book (AddressBook): The AddressBook to check for contact existence.
        """
        self.book = book
        super().__init__()

    def validate(self, document):
        """Validate the input document.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the contact doesn't exist in the AddressBook.
        """
        text = document.text

        if self.book.find_full_match(text) is None:
            raise ValidationError(message='Contact does not exist')


class SimpleListValidator(Validator):
    """Validator to check if the input text is in a list of items."""

    def __init__(self, items: list[str], allow_empty=False) -> None:
        """
        Initialize the validator with a list of valid items.

        Args:
            items (list): The list of valid items to compare against.
            allow_empty (bool): Whether an empty input is allowed.
        """
        self.items = items
        self.allow_empty = allow_empty
        super().__init__()

    def validate(self, document):
        """Validate the input document.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the input is not in the list of valid items.
        """
        text = document.text.strip()

        if self.allow_empty == True and len(text) == 0:
            return

        if text not in self.items:
            message = f'Provided text should be one item from the following list {str(self.items)}'
            raise ValidationError(message=message)


class PhoneValidator(Validator):
    """Validator to check the format of a phone number."""

    def validate(self, document):
        """Validate the input document for a valid phone number format.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the phone number format is invalid.
        """
        text = document.text.strip()

        if len(text) > 0 and (len(text) != 10 or not text.isdigit()):
            raise ValidationError(
                message='Invalid phone format. Phone should contain 10 digits.')


class EmailValidator(Validator):
    """Validator to check the format of an email address."""

    def validate(self, document):
        """Validate the input document for a valid email address format.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the email address format is invalid.
        """
        text = document.text

        pattern = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if len(text) > 0 and not re.match(pattern, text):
            raise ValidationError(
                message='Invalid email format.')


class DateValidator(Validator):
    """Validator to check the format of a date in DD.MM.YYYY format."""

    def validate(self, document):
        """Validate the input document for a valid date format.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the date format is invalid.
        """
        text = document.text
        if len(text) > 0:
            try:
                datetime.strptime(text, '%d.%m.%Y')
            except ValueError as e:
                raise ValidationError(
                    message='Invalid birthday format. Use DD.MM.YYYY') from e
