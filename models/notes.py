
from typing import Optional
from models.base_class import BaseClass


class Note:
    def __init__(self, title, text):
        self.id = 0
        self.title = title
        self.text = text

    def __repr__(self):
        return f"title: {self.title}\n\n{self.text}"


class Notes(BaseClass):
    _filename = 'notes.pcl'

    def __init__(self):
        super().__init__()
        self._cached_tags: Optional[list[str]] = None
        self.id_counter = 0

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle _cached_tags
        del state["_cached_tags"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._cached_tags = None

    def add(self, title: str, text: Optional[str]) -> Optional[Note]:
        note = Note(
            title=title,
            text=text
        )
        self.id_counter += 1
        note.id = self.id_counter
        self[note.title] = note
        self.update_tags()
        return note

    def find_notes(self, keyword):
        ret = []
        found_notes = [note for note in self.values() if keyword in note.title.lower() or keyword in note.text.lower()]
        for note in sorted(found_notes, key=lambda x: x.id):
            ret.append(note)
        return ret

    def find_full_match(self, keyword):
        found_notes = [note for note in self.values() if keyword == note.title]
        for note in sorted(found_notes, key=lambda x: x.id):
            if note is not None:
                return note

    def all_notes(self):
        ret = []
        for note in sorted(self.values(), key=lambda x: x.id):
            ret.append(note)
        return ret

    def remove_note(self, note) -> bool:
        self.update_tags()
        if self.data.pop(note.title) != None:
            return True
        else:
            return False

    def update_tags(self):
        self._cached_tags = None

    def find_notes_by_tag(self, tag) -> list[Note]:
        ret = []
        for note in self.values():
            if note.text is not None and tag in note.text:
                ret.append(note)
        return ret

# Tags

    def collect_tags(self) -> list[str]:  # Тимчасова база
        if self._cached_tags is not None:
            return self._cached_tags
        temp_tags = []
        for note in self.values():
            words = note.text.split()
            for word in words:
                if word.startswith('#'):
                    temp_tags.append(word[1:])
        return temp_tags

    def all_tags(self):  # Від найчастішого до найменьш вживанного
        tempo_tags = self.collect_tags()
        print(tempo_tags)
        sorted_tags = sorted(tempo_tags, reverse=True)
        return sorted_tags

    def all_tags_revert(self):  # Від найменьш вживанного до найчастішого
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(tempo_tags, reverse=False)
        return sorted_tags

    def alpsort_tags(self):  # Сортування за алфавітом: спершу числа, потім літери
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(
            tempo_tags, key=lambda x: (x.isnumeric(), x.lower()))
        return sorted_tags

    # Сортування за алфавітом: спершу останні літери, в конці цифри
    def alpsort_tags_revert(self):
        tempo_tags = self.collect_tags()
        sorted_tags = sorted(tempo_tags, key=lambda x: (
            x.isnumeric(), x.lower()), reverse=True)
        return sorted_tags

    def find_tag(self, query):  # Пошук записів по тегах у тексті
        if query.startswith("#"):
            query = query[1:]

        if len(query) > 127:
            print("The query is too long!")
            return

        matching_tags = {}

        for note in self.values():
            words = note.text.split()
            for word in words:
                if word.startswith('#'):
                    cleaned_word = word[1:]
                    if cleaned_word.startswith(query):
                        if cleaned_word not in matching_tags:
                            matching_tags[cleaned_word] = []
                        matching_tags[cleaned_word].append(note.title)

        sorted_tags = sorted(matching_tags.keys(),
                             key=lambda k: (len(k) - len(query), k))

        results = {}
        for tag in sorted_tags:
            results[tag] = []
            for title in matching_tags[tag]:
                results[tag].append(title)

        return results
