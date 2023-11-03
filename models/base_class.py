
from collections import UserDict
import pickle
from pathlib import Path
import os
from typing import Type


class BaseClass(UserDict):

    _filename: str = 'default.pcl'

    def save(self, filename = None):
        result = None
        if filename is None:
            filename = self.__class__.__get_model_path()
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    def __enter__(self):
        return self
         
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    @classmethod
    def load_or_create(cls, filename = None) -> Type:
        result = None
        if filename is None:
            filename = cls.__get_model_path()
        
        try:
            with open(filename, "rb") as file:
                result = pickle.load(file)
        except Exception:
            result = cls()
            result._load_demo_data()
        return result
    
    @classmethod
    def __get_model_path(cls) -> str:
        folder_path = os.path.join(Path.home(), '.team-6')
        if not os.path.exists(path=folder_path):
            os.mkdir(folder_path)
        return os.path.join(folder_path, cls._filename)
    
    def _load_demo_data(self):
        pass