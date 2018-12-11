import os
import dbm
import pickle
import numpy as np
from datetime import datetime
from settings import DATABASES_DIR


class DatabaseManager:

    class Manager:

        class ValueExistError(Exception):
            pass
        
        class DoesNotExistError(Exception):
            pass

        class IncorrectFormatError(Exception):
            pass

        def __init__(self, db):
            self.db = db

        def items(self):
            objects = []
            for key in self.db.keys():
                objects.append((key.decode('ascii'), pickle.loads(self.db[key])))
            return objects
        
        def create(self, id, obj):
            if id in self.db:
                raise self.ValueExistError()
            self.db[id] = pickle.dumps(obj)
            return obj
        
        def read(self, id):
            if id not in self.db:
                raise self.DoesNotExistError()
            return pickle.loads(self.db[id])
        
        def update(self, id, obj):
            if id not in self.db:
                raise self.DoesNotExistError()
            self.db[id] = pickle.dumps(obj)
            return obj
        
        def delete(self, id):
            if id not in self.db:
                raise self.DoesNotExistError()
            obj = pickle.loads(self.db[id])
            del self.db[id]
            return obj
        
        @staticmethod
        def validate(obj, format):
            if format is None or type(format) is not dict:
                return False
            r = True
            r = r and set(obj.keys()) == set(format.keys())
            for key in obj:
                r = r and (type(obj[key]) is format[key] or type(obj[key]) == type(format[key]))
                if not r:
                    break
            return r

    def __init__(self, db_name):
        self.db_name = db_name
    
    def __enter__(self):
        self.db = dbm.open(os.path.join(DATABASES_DIR, self.db_name), 'c')
        return DatabaseManager.Manager(self.db)

    def __exit__(self, exception_type, exception_value, traceback):
        self.db.close()


class PersonsDatabase(DatabaseManager):

    DEFAULT_FILE_NAME = 'persons'

    class Manager(DatabaseManager.Manager):

        FORMAT = {
            'name': str,
            'surname': str,
        }

        def items(self):
            return super().items()

        def create(self, id, obj):
            if not DatabaseManager.Manager.validate(obj, self.FORMAT):
                raise self.IncorrectFormatError()
            return super().create(id, obj)
        
        def read(self, id):
            return super().read(id)

        def update(self, id, obj):
            if not DatabaseManager.Manager.validate(obj, self.FORMAT):
                raise self.IncorrectFormatError()
            return super().update(id, obj)
        
        def delete(self, id):
            return super().delete(id)

        def __init__(self, db):
            return super().__init__(db)

    def __init__(self, db_name=DEFAULT_FILE_NAME):
        return super().__init__(db_name)

    def __enter__(self):
        manager = super().__enter__()
        manager.__class__ = PersonsDatabase.Manager
        return manager


class FacesDatabase(DatabaseManager):

    DEFAULT_FILE_NAME = 'faces'

    class Manager(DatabaseManager.Manager):

        FORMAT = {
            'person_id': str,
            'encoding': np.array([]),
            'updated': datetime
        }

        def items(self):
            return super().items()

        def create(self, id, obj):
            if not DatabaseManager.Manager.validate(obj, self.FORMAT):
                raise self.IncorrectFormatError()
            return super().create(id, obj)
        
        def read(self, id):
            return super().read(id)

        def update(self, id, obj):
            if not DatabaseManager.Manager.validate(obj, self.FORMAT):
                raise self.IncorrectFormatError()
            return super().update(id, obj)
        
        def delete(self, id):
            return super().delete(id)

        def __init__(self, db):
            return super().__init__(db)

    def __init__(self, db_name=DEFAULT_FILE_NAME):
        return super().__init__(db_name)

    def __enter__(self):
        manager = super().__enter__()
        manager.__class__ = FacesDatabase.Manager
        return manager