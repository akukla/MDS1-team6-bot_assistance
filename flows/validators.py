
from prompt_toolkit.validation import Validator, ValidationError
from models.address_book import AddressBook
import re
from datetime import datetime

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


 # class PhoneValidator(Validator):

     # def validate(self, document):
         # text = document.text

        #  # TODO: Implement this method
        #  if len(text.strip()) > 0 and len(text.strip()) != 10:
            #  raise ValidationError(message='Invalid phone format. Phone should contain 10 digits.')
        
 #  Class Phone  validator     
class PhoneValidator(Validator):       
        
    def validate(self, document):
        text = document.text.strip()

        # Check if the text is not empty and if it does not contain exactly 10 digits
        if len(text) > 0 and not re.fullmatch(r'\d{10}', text):
            raise ValidationError(message='Invalid phone format. Phone should contain 10 digits.')

# Class Email validator  
class EmailValidator(Validator):

    def validate(self, document):
        text = document.text.strip()

        # TODO: Implement this method
# Validate the email using a regex
        if len(text) > 0  and not re.fullmatch(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
            raise ValidationError(message='Invalid email format.')


# Class Date validator  
class DateValidator(Validator):
  
    def validate(self, document):
        text = document.text.strip()
        # Validate the date using datetime.strptime()
       # if len(text) > 0:
           # try:
               # datetime.strptime(text, '%d.%m.%Y')
      #      except ValueError:
         #       raise ValidationError(f"Birthday must be in the format DD.MM.YYYY.")