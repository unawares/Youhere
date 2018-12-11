import os
import dbm
import pickle
from datetime import datetime
from settings import SESSIONS_DIR
from manager import DatabaseManager

class SessionsManager(DatabaseManager):

    class Manager(DatabaseManager.Manager):
        pass

    def __init__(self, db_name):
        return super().__init__(db_name)

    def __enter__(self):
        self.db = dbm.open(os.path.join(SESSIONS_DIR, self.db_name), 'c')
        return SessionsManager.Manager(self.db)

    def __exit__(self, exception_type, exception_value, traceback):
        self.db.close()


class FoundsSession(SessionsManager):

    DEFAULT_FILE_NAME = 'founds'

    class Manager(SessionsManager.Manager):

        FORMAT = {
            'face_id': str,
            'place': str,
            'camera': str,
            'date': datetime,
        }

        def list(self):
            return super().list()

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
        manager.__class__ = FoundsSession.Manager
        return manager


class HistorySession(SessionsManager):

    DEFAULT_FILE_NAME = 'history'

    class Manager(SessionsManager.Manager):

        FORMAT = {
            'found_ids': list,
        }

        def list(self):
            return super().list()

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
        manager.__class__ = HistorySession.Manager
        return manager