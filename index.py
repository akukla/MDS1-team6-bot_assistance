from models.address_book import AddressBook
from actions import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book: AddressBook = AddressBook.load_or_create()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        should_save = False

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
            should_save = True
        elif command == "change":
            print(change_contact(args, book))
            should_save = True
        elif command == "phone":
            print(get_contact(args, book))
        elif command == "all":
            print(get_all_contact(args, book))
        elif command == "birthdays":
            print(print_birthdays(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
            should_save = True
        elif command == "show-birthday":
            print(show_birthday(args, book))
            should_save = True
        else:
            print("Invalid command.")

        if should_save:
            book.save()


if __name__ == "__main__":
    main()
