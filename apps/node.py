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

class Node(Base):

    FUNCTIONS = ['found']

    class Actions(Base.Actions):

        def found(self, place, camera, face_encodings):
            def add_to_history(key, found):
                with HistorySession() as manager:
                    if found[1]['person_id'] not in manager.db:
                        manager.create(found[1]['person_id'], {
                            'found_ids': []
                        })
                    val = manager.read(found[1]['person_id'])
                    val['found_ids'].append(key)
                    manager.update(found[1]['person_id'], val)
            def found_face_object(found):
                with FoundsSession() as manager:
                    key = generate_random_key()
                    manager.create(key, {
                        'face_id': found[0],
                        'place': place,
                        'camera': camera,
                        'date': datetime.now()
                    })
                    add_to_history(key, found)
            with FacesDatabase() as manager:
                objects = manager.items()
                known_face_encodings = list(map(lambda v: v[1]['encoding'], objects))
                for face_encoding in face_encodings:
                    results = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    if True in results:
                        index = results.index(True)
                        found_face_object(objects[index])
            return 'Counted'