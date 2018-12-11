import socket
import time
from client import (
    Client, Terminal
)

class User(Client):

    def loop(self):
        pass

class UserTerminal(Terminal):

    def loop(self):
        name = input('Name: ')
        surname = input('Surname: ')
        self.client.connection.send({
            'app': 'client',
            'function': 'last_view',
            'args': [],
            'kwargs': {
                'name': name,
                'surname': surname,
            },
        })
        connection, response = self.read()
        if 'result' in response:
            result = response['result']
            print('--------------------')
            print('%s %s' % (result['person']['name'], result['person']['surname']))
            print('Place: %s' % (result['found']['place'],))
            print('Camera: %s' % (result['found']['camera'],))
            print('Date: %s' % (result['found']['date'],))
            print('--------------------')
            print()
        else:
            print('Unknown')

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8080))
    terminal = UserTerminal()
    client = User(terminal, sock)
    client.mainloop()