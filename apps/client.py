import face_recognition
from datetime import datetime
from .base import Base
from manager import (
    FacesDatabase, PersonsDatabase
)
from sessions import (
    FoundsSession, HistorySession
)
from utils import (
    generate_key,
    generate_random_key
)

class Client(Base):

    FUNCTIONS = ['view']

    class Actions(Base.Actions):

        def last_view(self, name, surname):
            key = generate_key(name, surname)
            with HistorySession() as manager:
                history = manager.read(key)
                last_found_id = history['found_ids'][-1]
            with FoundsSession() as manager:
                found = manager.read(last_found_id)
            with FacesDatabase() as manager:
                face = manager.read(found['face_id'])
            with PersonsDatabase() as manager:
                person = manager.read(face['person_id'])
            return {
                'person': person,
                'found': found,
                'face': face,
            }