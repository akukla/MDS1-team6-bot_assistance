
from models.base_class import BaseClass

class Note:
    id_counter = max(note['id'] for note in notes) 

    def __init__(self, title, text):
        self.id = Note.id_counter
        Note.id_counter += 1
        self.title = title
        self.text = text

    def __repr__(self):
        return f"ID: {self.id}, Title: {self.title}, \nText: {self.text}"

class Notes(BaseClass):
    _filename = 'notes.pcl'

    def __init__(self):
        super().__init__()
        self.notes = self.data.get('notes', [])

    def add_note(self):
        title = input("Enter the title (max 64 chars, no tags): ")[:64]
        if not title.isascii():
            print("Title should be in English.")
            return
        text = input("Enter the main text (Add # before a word if you want to make it a tag): ")
        if not text.isascii():
            print("Text should be in English.")
            return
        note = Note(title, text)
        self.notes.append(note)
        self.data['notes'] = self.notes
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

# Tags

    def collect_tags(self): # Тимчасова база
        tempo_tags = {}
        for note in self.notes:
            words = note.text.split()
            for word in words:
                if word.startswith('#'):
                    tempo_tags[word] = tempo_tags.get(word, 0) + 1
            return tempo_tags
        
    def all_tags(self): # Від найчастішого до найменьш вживанного
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(tempo_tags.items(), key=lambda x: x[1], reverse=True)
        return sorted_tags   
    
    def all_tags_revert(self): # Від найменьш вживанного до найчастішого
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(tempo_tags.items(), key=lambda x: x[1], reverse=False)
        return sorted_tags
    
    def alpsort_tags(self): # Сортування за алфавітом: спершу числа, потім літери
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(tempo_tags.items(), key=lambda x: (x[0].isnumeric(), x[0].lower()))
        return sorted_tags
    
    def alpsort_tags_revert(self): # Сортування за алфавітом: спершу останні літери, в конці цифри
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(tempo_tags.items(), key=lambda x: (x[0].isnumeric(), x[0].lower()), reverse=True)
        return sorted_tags
    
    def find_tag(self, query): # Пошук записів по тегах у тексті
        if query.startswith("#"):
            query = query[1:]

        if len(query) > 127:
            print("The query is too long!")
            return
            
        matching_tags = {}

        for note in self.notes:
            words = note.text.split()
            for word in words:
                if word.startswith('#'):
                    cleaned_word = word[1:]
                    if cleaned_word.startswith(query):
                        if cleaned_word not in matching_tags:
                            matching_tags[cleaned_word] = []
                        matching_tags[cleaned_word].append(note.title)

        sorted_tags = sorted(matching_tags.keys(), key=lambda k: (len(k) - len(query), k))

        results = []
        for tag in sorted_tags:
            results.append(f"Tag: #{tag}")
            for title in matching_tags[tag]:
                results.append(f" - {title}")

        return results
 
        

notes_module = Notes.load_or_create()