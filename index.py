from models.address_book import AddressBook
from models.notes import Notes
from actions import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    with AddressBook.load_or_create() as book, Notes.load_or_create() as notes:

        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(get_contact(args, book))
            elif command == "all":
                print(get_all_contact(args, book))
            elif command == "birthdays":
                print(print_birthdays(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
