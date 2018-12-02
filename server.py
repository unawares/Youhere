import types
import socket
import selectors
import time

from utils import is_valid_request, is_valid_response

from connection import Selector

from app import App

HOST = '127.0.0.1'
PORT = 8080

app = App()

def server(host, port):
    selector = selectors.DefaultSelector()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.setblocking(False)
    selector.register(server_socket, selectors.EVENT_READ, data=None)
    return server_socket, selector

server_socket, server_selector = server(HOST, PORT)
selector = Selector()

def reader(conenction, obj):
    try:
        if is_valid_request(obj):
            print('Request from', conenction.address, repr(obj))
            response = app.serve(obj)
            if is_valid_response(response):
                conenction.send(response)
            else:
                conenction.send('Internal Error')
        else:
            conenction.send('Invalid Format')
    except Exception as err:
        conenction.send('Error occured: ' + str(err))


print('Listening on', (HOST, PORT))
while True:
    try:
        requests = server_selector.select(timeout=0.001)
        for key, mask in requests:
            socket = key.fileobj
            socket, address = socket.accept()
            connection = selector.register(socket, address)
            connection.reader(reader)
        selector.step()
    except Exception:
        pass
    except KeyboardInterrupt:
        server_socket.close()
        exit()