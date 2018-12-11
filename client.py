import socket
import threading
import time
import face_recognition
import cv2
import numpy as np
from urllib.request import urlopen
from connection import Selector


class Client:
    
    def __init__(self, terminal, socket):
        self.terminal = terminal
        self.selector = Selector()
        self.connection = self.selector.register(socket, socket.getsockname())
        self.delay = 0.0001
        self.terminal.init(self)

    def loop(self):
        pass

    def mainloop(self):
        try:
            self.terminal.start()
            while True:
                self.selector.step()
                self.loop()
                time.sleep(self.delay)
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        finally:
            self.terminal.stop()
            self.terminal.destroy()
        

class Terminal(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.active = False
        self.client = None
        self.delay = 0.0001
        self.responses = []

    def init(self, client):
        self.client = client
        self.client.connection.reader(self.reader)

    def loop(self):
        pass

    def read(self):
        while len(self.responses) == 0:
            time.sleep(self.delay)
        return self.responses.pop(0)

    def reader(self, connection, response):
        self.responses.append((connection, response))

    def destroy(self):
        self.client.connection.remove()
        self.client = None

    def start(self):
        self.active = True
        return super().start()

    def stop(self):
        self.active = False

    def run(self):
        while True:
            if self.client is None:
                raise Exception('Not initiated')
            self.loop()
            time.sleep(self.delay)
