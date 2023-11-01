from flows.address_book_flows import flow_contact_add, flow_contact_edit, flow_contact_remove
from flows.common_flow import get_main_completion, parse_input
from models.address_book import AddressBook
from models.notes import Notes
from actions import *
from prompt_toolkit import prompt

from flows.validators import *
from prompt_toolkit import PromptSession


def invalid_command_action():
    print("Invalid command.")


def main():
    session = PromptSession()
    with AddressBook.load_or_create() as book, Notes.load_or_create() as notes:

        completer = get_main_completion(book=book, notes=notes)

        print("Welcome to the assistant bot!")
        while True:

            user_input = session.prompt('Enter a command: ', completer=completer)
            module, command, *args = parse_input(user_input)

            if command in ["close", "exit", "quit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "help":
                # TODO: Implement help information
                print("Help is not implemented right now")
            elif module == 'contacts':
                if command == 'add':
                    print(flow_contact_add(book))
                elif command == "all":
                    print(get_all_contacts(book))
                elif command == 'edit':
                    if len(args) > 0 and args[0] is not None and book.find_full_match(args[0]) is not None:
                        print(flow_contact_edit(book, args))
                    else:
                        print("Provide valid contact name to edit")
                elif command == 'remove':
                    if len(args) > 0 and args[0] is not None and book.find_full_match(args[0]) is not None:
                        record = book.find_full_match(args[0])
                        print(flow_contact_remove(book, record))
                    else:
                        print("Provide valid contact name to remove. Valid format is: contacts remove \"NAME\"")
                elif command == 'find':
                    # TODO: Implement find flow
                    print("Find is not implemented")
                elif command == 'birthdays':
                    # TODO: Implement birthdays flow
                    print("Birthdays is not implemented")
                else:
                    invalid_command_action()
            else:
                invalid_command_action()

        # print("Welcome to the assistant bot!")
        # while True:
        #     user_input = input("Enter a command: ")
        #     command, *args = parse_input(user_input)

        #     if command in ["close", "exit"]:
        #         print("Good bye!")
        #         break
        #     elif command == "hello":
        #         print("How can I help you?")
        #     elif command == "add":
        #         print(add_contact(args, book))
        #     elif command == "change":
        #         print(change_contact(args, book))
        #     elif command == "phone":
        #         print(get_contact(args, book))
        #     elif command == "all":
        #         print(get_all_contact(args, book))
        #     elif command == "birthdays":
        #         print(print_birthdays(args, book))
        #     elif command == "add-birthday":
        #         print(add_birthday(args, book))
        #     elif command == "show-birthday":
        #         print(show_birthday(args, book))
        #     else:
        #         print("Invalid command.")


if __name__ == "__main__":
    main()
