
from models.base_class import BaseClass

class Note:
    id_counter = 1 

    def __init__(self, title, text):
        self.id = Note.id_counter
        Note.id_counter += 1
        self.title = title
        self.text = text

    def __repr__(self):
        return f"ID: {self.id}, Title: {self.title}, Text: {self.text}"

class Notes(BaseClass):
    _filename = 'notes.pcl'

    def __init__(self):
        super().__init__()
        self.notes = self.data.get('notes', [])

    def add_note(self):
        title = input("Enter the title (max 64 chars): ")[:64]
        if not title.isascii():
            print("Title should be in English.")
            return
        text = input("Enter the main text: ")
        if not text.isascii():
            print("Text should be in English.")
            return
        note = Note(title, text)
        self.notes.append(note)
        self.data['notes'] = self.notes
        self.save()
        print(f"Note with ID {note.id} added!")

    def find_note(self, keyword):
        found_notes = [note for note in self.notes if keyword in note.title]
        for note in sorted(found_notes, key=lambda x: x.id):
            print(note)

    def delete_note(self, note_id):
        note_to_delete = next((note for note in self.notes if note.id == note_id), None)
        if not note_to_delete:
            print(f"No note with ID {note_id} found.")
            return
        confirm = input(f"Do you really want to delete note with ID {note_id}? (yes/no) ")
        if confirm.lower() == 'yes':
            self.notes.remove(note_to_delete)
            self.data['notes'] = self.notes
            self.save()
            print("Note deleted!")

    def edit_note(self, note_id):
        note_to_edit = next((note for note in self.notes if note.id == note_id), None)
        if not note_to_edit:
            print(f"No note with ID {note_id} found.")
            return
        new_title = input(f"Current title is {note_to_edit.title}. Enter new title or press Enter to skip: ")
        if new_title:
            if not new_title.isascii():
                print("Title should be in English.")
                return
            note_to_edit.title = new_title
        new_text = input(f"Current text is {note_to_edit.text}. Enter new text or press Enter to skip: ")
        if new_text:
            if not new_text.isascii():
                print("Text should be in English.")
                return
            note_to_edit.text = new_text
        self.data['notes'] = self.notes
        self.save()
        print("Note updated!")


notes_module = Notes.load_or_create()