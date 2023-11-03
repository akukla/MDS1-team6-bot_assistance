# goitneo-python-final-project-team-6

This is final project for Team 6

## Installation

This project required Python 3.11+

Install pakages

```
pip3 install -r requirements.txt
```

## Run bot

```
python index.py
This is a simple assistant bot designed to help you manage your contacts and notes.

Autocompletion is available for all commands. To use autocomplete, simply press the arrow keys to navigate through the suggestions and hit space to confirm your selection.

**Command Examples:**
- `contacts all`: Show all contacts.
- `contacts edit "John Doe"`: Edit the contact named "John Doe".
- `notes all`: Show all notes.
- `notes remove "Note Title"`: Remove the note titled "Note Title".

**Available Commands:**
- **contacts**
    - `add`: Add a new contact.
    - `all`: Show all contacts.
    - `edit "CONTACT_NAME"`: Edit the specified contact.
    - `remove "CONTACT_NAME"`: Remove the specified contact.
    - `find`: Search for a contact.
    - `birthdays "DAYS"`: Show contacts with birthdays in the specified number of days.

- **notes**
    - `add`: Create a new note.
    - `all`: Show all notes.
    - `find "NOTE_TITLE"`: Find a note by its title.
    - `remove "NOTE_TITLE"`: Remove the note with the specified title.
    - `edit "NOTE_TITLE"`: Edit the note with the specified title.

- **tags**
    - `find_by_tag`: Find and sort notes by tag.
    - `all_tags`: [print all tags]
    - `all_tags_revert`: [Print all tags in reverted order]
    - `alpsort_tags`: [Print tax as aper alphavitical order]
    - `alpsort_tags_revert`: [Upsort alphaveitclal order]

- `help`: Show this help text.
- `exit`, `close`, or `quit`: Exit the application.

# Note Management System

This guide provides a detailed explanation of the functionalities available in the Note Management System.

## Functions

### **1. Add Note**
#### `flow_note_add(notes: Notes) -> str`
   - **Purpose**: Adds a new note to the collection.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Prompts the user for a title and text for the new note. If the title input is empty, the operation is canceled.
   - **Returns**: A message indicating whether the note was added or not.

### **2. Show Note**
#### `flow_note_show(note: Note) -> str`
   - **Purpose**: Displays a specific note.
   - **Arguments**: `note` - The note to display.
   - **Behavior**: Formats and displays the note's content.
   - **Returns**: A string representation of the note.

### **3. Find Note**
#### `flow_note_find(notes: Notes, term: str) -> str`
   - **Purpose**: Searches for notes containing a specific term.
   - **Arguments**: `notes` - An instance of the Notes class, `term` - The search term.
   - **Behavior**: Searches the collection and returns notes containing the term.
   - **Returns**: A string with matching notes separated by `-----`.

### **4. Remove Note**
#### `flow_note_remove(notes: Notes, note: Note) -> str`
   - **Purpose**: Removes a specified note.
   - **Arguments**: `notes` - An instance of the Notes class, `note` - The note to remove.
   - **Behavior**: Asks for confirmation before removing the note.
   - **Returns**: A message indicating the outcome of the operation.

### **5. Edit Note**
#### `flow_note_edit(notes: Notes, note: Note) -> str`
   - **Purpose**: Edits the title and text of a specific note.
   - **Arguments**: `notes` - An instance of the Notes class, `note` - The note to edit.
   - **Behavior**: Prompts the user to confirm and input changes for the title and text.
   - **Returns**: A message indicating whether the note was updated or not.

### **6. List All Notes**
#### `flow_note_all(notes: Notes) -> str`
   - **Purpose**: Lists all the notes.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all notes in the collection.
   - **Returns**: A string with all notes separated by `-----`.

### **7. Find By Tag**
#### `flow_tags_find_by_tag(notes: Notes, args: list[Optional[str]]) -> str`
   - **Purpose**: Finds notes associated with a specific tag.
   - **Arguments**: `notes` - An instance of the Notes class, `args` - A list containing the tag to search for.
   - **Behavior**: Searches for and lists notes containing the specified tag.
   - **Returns**: A string representation of the notes with the tag.

### **8. List All Tags**
#### `flow_tags_all_tags(notes: Notes) -> str`
   - **Purpose**: Lists all tags in the collection.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags.
   - **Returns**: A string representation of all tags.

### **9. List All Tags (Reversed)**
#### `flow_tags_all_tags_revert(notes: Notes) -> str`
   - **Purpose**: Lists all tags in reverse order.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags in reverse order.
   - **Returns**: A string representation of all tags in reverse.

### **10. Alphabetically Sort Tags**
#### `flow_tags_alpsort_tags(notes: Notes) -> str`
   - **Purpose**: Lists tags in alphabetical order.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags alphabetically.
   - **Returns**: A string representation of the tags in alphabetical order.

### **11. Alphabetically Sort Tags (Reversed)**
#### `flow_tags_alpsort_tags_revert(notes: Notes) -> str`
   - **Purpose**: Lists tags in reverse alphabetical order.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags in reverse alphabetical order.
   - **Returns**: A string representation of the tags in reverse alphabetical order.

## Usage

To utilize these functions, ensure you have an instance of `Notes` available and call the desired function as needed.

```python
notes = Notes()
flow_note_add(notes)

# Note Management System

This guide provides a detailed explanation of the functionalities available in the Note Management System.

## Functions

### **1. Add Note**
#### `flow_note_add(notes: Notes) -> str`
   - **Purpose**: Adds a new note to the collection.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Prompts the user for a title and text for the new note. If the title input is empty, the operation is canceled.
   - **Returns**: A message indicating whether the note was added or not.

### **2. Show Note**
#### `flow_note_show(note: Note) -> str`
   - **Purpose**: Displays a specific note.
   - **Arguments**: `note` - The note to display.
   - **Behavior**: Formats and displays the note's content.
   - **Returns**: A string representation of the note.

### **3. Find Note**
#### `flow_note_find(notes: Notes, term: str) -> str`
   - **Purpose**: Searches for notes containing a specific term.
   - **Arguments**: `notes` - An instance of the Notes class, `term` - The search term.
   - **Behavior**: Searches the collection and returns notes containing the term.
   - **Returns**: A string with matching notes separated by `-----`.

### **4. Remove Note**
#### `flow_note_remove(notes: Notes, note: Note) -> str`
   - **Purpose**: Removes a specified note.
   - **Arguments**: `notes` - An instance of the Notes class, `note` - The note to remove.
   - **Behavior**: Asks for confirmation before removing the note.
   - **Returns**: A message indicating the outcome of the operation.

### **5. Edit Note**
#### `flow_note_edit(notes: Notes, note: Note) -> str`
   - **Purpose**: Edits the title and text of a specific note.
   - **Arguments**: `notes` - An instance of the Notes class, `note` - The note to edit.
   - **Behavior**: Prompts the user to confirm and input changes for the title and text.
   - **Returns**: A message indicating whether the note was updated or not.

### **6. List All Notes**
#### `flow_note_all(notes: Notes) -> str`
   - **Purpose**: Lists all the notes.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all notes in the collection.
   - **Returns**: A string with all notes separated by `-----`.

### **7. Find By Tag**
#### `flow_tags_find_by_tag(notes: Notes, args: list[Optional[str]]) -> str`
   - **Purpose**: Finds notes associated with a specific tag.
   - **Arguments**: `notes` - An instance of the Notes class, `args` - A list containing the tag to search for.
   - **Behavior**: Searches for and lists notes containing the specified tag.
   - **Returns**: A string representation of the notes with the tag.

### **8. List All Tags**
#### `flow_tags_all_tags(notes: Notes) -> str`
   - **Purpose**: Lists all tags in the collection.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags.
   - **Returns**: A string representation of all tags.

### **9. List All Tags (Reversed)**
#### `flow_tags_all_tags_revert(notes: Notes) -> str`
   - **Purpose**: Lists all tags in reverse order.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags in reverse order.
   - **Returns**: A string representation of all tags in reverse.

### **10. Alphabetically Sort Tags**
#### `flow_tags_alpsort_tags(notes: Notes) -> str`
   - **Purpose**: Lists tags in alphabetical order.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags alphabetically.
   - **Returns**: A string representation of the tags in alphabetical order.

### **11. Alphabetically Sort Tags (Reversed)**
#### `flow_tags_alpsort_tags_revert(notes: Notes) -> str`
   - **Purpose**: Lists tags in reverse alphabetical order.
   - **Arguments**: `notes` - An instance of the Notes class.
   - **Behavior**: Lists all tags in reverse alphabetical order.
   - **Returns**: A string representation of the tags in reverse alphabetical order.

## Usage

To utilize these functions, ensure you have an instance of `Notes` available and call the desired function as needed.

```python
notes = Notes()
flow_note_add(notes)
# **Address Book Bot Functions**

## **1. Initialization and Setup**

### `AddressBook()`
- **Description**: Initializes an instance of the Address Book.

## **2. Contact Management**

### `add_contact(name, phone=None, email=None, address=None, birthday=None)`
- **Description**: Adds a new contact to the Address Book.
- **Parameters**:
    - `name` (str): Name of the contact.
    - `phone` (str, optional): Phone number of the contact.
    - `email` (str, optional): Email address of the contact.
    - `address` (str, optional): Physical address of the contact.
    - `birthday` (str, optional): Birthday of the contact in "DD.MM.YYYY" format.

### `delete(name)`
- **Description**: Deletes a contact by name from the Address Book.
- **Parameters**:
    - `name` (str): Name of the contact to delete.

### `_load_demo_data()`
- **Description**: Populates the Address Book with demo data.

## **3. Contact Search and Retrieval**

### `find_full_match(name)`
- **Description**: Finds and returns a contact by exact name match.
- **Parameters**:
    - `name` (str): Name of the contact to find.

### `find(term)`
- **Description**: Finds and returns a list of contacts that partially match the search term in the name.
- **Parameters**:
    - `term` (str): Search term.

### `find_by(field, value)`
- **Description**: Searches for contacts based on a specific field and value.
- **Parameters**:
    - `field` (str): The field to search (e.g., "name", "phone", "birthday", "email", "address").
    - `value` (str): The value to search for in the specified field.

### `enumerate()`
- **Description**: Enumerates through all the contacts in the Address Book.

### `__len__()`
- **Description**: Returns the total number of contacts in the Address Book.

## **4. Birthday Notifications**

### `get_birthdays(delta_days)`
- **Description**: Retrieves contacts that have birthdays within a specified number of days.
- **Parameters**:
    - `delta_days` (int): Number of days from today to search for upcoming birthdays.
