import socket
import threading
import time
import face_recognition
import cv2
import numpy as np
from urllib.request import urlopen
from connection import Selector


WINDOW_HEIGHT = 560

class Camera(threading.Thread):
    
    def __init__(self, url, interval):
        threading.Thread.__init__(self)
        self.url = url
        self.frame = None
        self.last_frame = None
        self.face_locations = []
        self.face_encodings = []
        self.interval = interval
        self.active = False
        self.delay = 0.0001

    def run(self):
        counter = 0
        while self.active:
            counter += 1
            imgNp = np.array(bytearray(urlopen(self.url).read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            self.frame = img
            if counter == self.interval:
                self.parse()
                counter = 0
            time.sleep(self.delay)
    
    def start(self):
        self.active = True
        return super().start()

    def stop(self):
        self.active = False
    
    def parse(self):
        self.last_frame = self.frame.copy()
        self.face_locations = face_recognition.face_locations(self.last_frame)
        self.face_encodings = face_recognition.face_encodings(self.last_frame, self.face_locations)

    def last(self):
        return self.last_frame, self.face_locations, self.face_encodings

    def next(self):
        return self.frame


class Node:
    
    def __init__(self, terminal, socket):
        self.terminal = terminal
        self.terminal.init(self)
        self.sent = {}
        self.cameras = []
        self.selector = Selector()
        self.connection = self.selector.register(socket, socket.getsockname())
        self.delay = 0.0001

    def add(self, url):
        camera = Camera(url, 3)
        camera.setDaemon(True)
        camera.start()
        self.cameras.append(camera)
    
    def remove(self, url):
        for camera in self.cameras:
            if camera.url == url:
                camera.stop()
                try:
                    cv2.destroyWindow(camera.url)
                finally:
                    pass
    
    def send(self, face_encodings):
        self.connection.send({
            'app': 'node',
            'function': 'found',
            'args': [],
            'kwargs': {
                'face_encodings': face_encodings
            }
        })

    def mainloop(self):
        try:
            self.terminal.start()
            while True:
                for camera in self.cameras:
                    if not camera.active:
                        continue
                    last_frame, face_locations, face_encodings = camera.last()
                    frame = camera.next()
                    if frame is not None:
                        frame = frame.copy()
                        if face_locations is not None:
                            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        height, width = frame.shape[:2]
                        frame = cv2.resize(frame, (int(WINDOW_HEIGHT / height * width), WINDOW_HEIGHT))
                        cv2.imshow(camera.url, frame)
                        cv2.waitKey(1)
                    if camera.url not in self.sent or last_frame is not self.sent[camera.url][0]:
                        if camera.url not in self.sent and len(face_locations) > 0:
                            self.send(face_encodings)
                            self.sent[camera.url] = [last_frame, face_locations, face_encodings]
                        elif len(face_locations) > 0:
                            matches = face_recognition.compare_faces(self.sent[camera.url][2], face_encoding)
                            new_face_encodings = []
                            for face_encoding, match in zip(face_encodings, matches):
                                if not match:
                                    new_face_encodings.append(face_encoding)
                            if len(new_face_encodings) > 0:
                                self.send(new_face_encodings)
                                self.sent[camera.url] = [last_frame, face_locations, face_encodings]
                self.selector.step()
                time.sleep(self.delay)
        except KeyboardInterrupt:
            for camera in self.cameras:
                camera.stop()
                try:
                    cv2.destroyWindow(camera.url)
                finally:
                    pass
            self.cameras = []
            raise KeyboardInterrupt()
        finally:
            cv2.destroyAllWindows()
            self.terminal.stop()
            self.terminal.destroy()
        

class Terminal(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.active = False
        self.node = None

    def init(self, node):
        self.node = node
    
    def destroy(self):
        self.node = None

    def start(self):
        self.active = True
        return super().start()

    def stop(self):
        self.active = False

    def run(self):
        while True:
            if self.node is None:
                raise Exception('Not initiated')
            print('[a] Add camera')
            print('[b] Remove camera')
            choice = input('Choice: ')
            if choice == 'a':
                self.node.add(self.get_url(input('host: ').strip()))
            elif choice == 'b':
                self.node.remove(self.get_url(input('host: ').strip()))
        
    def get_url(self, host):
        return 'http://' + host + '/shot.jpg'
            

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8080))
    terminal = Terminal()
    node = Node(terminal, sock)
    node.mainloop()

