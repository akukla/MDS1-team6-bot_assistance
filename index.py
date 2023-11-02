from flows.address_book_flows import flow_contact_add, flow_contact_birthdays, flow_contact_edit, flow_contact_find, flow_contact_remove
from flows.notes_flows import *
from flows.common_flow import get_main_completion, parse_input, help_text
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
                print(help_text)
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
                    if len(args) == 1 and args[0] is not None:
                        print(flow_contact_find(book, args[0]))
                    else:
                        print("Provide valid contact name to remove. Valid format is: contacts remove \"NAME\"")
                elif command == 'birthdays':
                    flow_contact_birthdays(book, args=args)
                else:
                    invalid_command_action()
            elif module == 'notes':
                if command == 'add':
                    print(flow_note_add(notes))
                elif command == 'all':
                    print(flow_note_all(notes))
                elif command == 'find':
                    if len(args) > 0 and args[0] is not None:
                        print(flow_note_find(notes, args[0]))
                    else:
                        print("Provide valid note title. Valid command format is: notes find \"NAME\"")
                elif command == 'remove':
                    if len(args) == 1 and args[0] is not None and notes.find_full_match(args[0]) is not None:
                        note = notes.find_full_match(args[0])
                        print(flow_note_remove(notes, note))
                    else:
                        print("Provide valid note title. Valid command format is: notes remove \"NAME\"")
                elif command == 'edit':
                    if len(args) == 1 and args[0] is not None and notes.find_full_match(args[0]) is not None:
                        note = notes.find_full_match(args[0])
                        print(flow_note_edit(notes, note))
                    else:
                        print("Provide valid note title. Valid command format is: notes edit \"NAME\"")
                else:
                    invalid_command_action()

            elif module == 'tags':
                if command == 'find_by_tag':
                    print(flow_tags_find_by_tag(notes, args))
                elif command == 'all_tags':
                    print(flow_tags_all_tags(notes))
                elif command == 'all_tags_revert':
                    print(flow_tags_all_tags_revert(notes))
                elif command == 'alpsort_tags':
                    print(flow_tags_alpsort_tags(notes))
                elif command == 'alpsort_tags_revert':
                    print(flow_tags_alpsort_tags_revert(notes))
                else:
                    invalid_command_action()
            else:
                invalid_command_action()


if __name__ == "__main__":
    main()
