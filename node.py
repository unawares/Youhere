import socket
import time
from connection import Selector

selector = Selector()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8080))
connection = selector.register(sock, sock.getsockname())

def read(connection, obj):
    print(obj)

connection.reader(read)

while True:
    time.sleep(0.001)
    connection.send({
        'app': 'node',
        'function': 'func',
        'args': [],
        'kwargs': {}
    })
    selector.step()


