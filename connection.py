import selectors
import socket
import types
import pickle


class Stream:

    def __init__(self):
        self.messages = []
        self.read = []

    def push(self, message):
        length = len(message)
        self.messages.append({
            'message': length.to_bytes(8, byteorder='big'),
        })
        self.messages.append({
            'message': message
        })
    
    def pop(self):
        if len(self.read) > 0 and self.read[0]['length'] == 0:
            return self.read.pop(0)
        return None
            

class Connection:

    def __init__(self, address):
        self.address = address
        self.stream = Stream()
        self.listener = None

    def send(self, obj):
        self.stream.push(pickle.dumps(obj))

    def reader(self, func):
        self.listener = func

    def remove(self):
        self.listener = None

    def emit(self, message):
        if type(self.listener) is types.FunctionType:
            self.listener(self, pickle.loads(message))
    
    
class Selector:
    
    def __init__(self, selector=selectors.DefaultSelector()):
        self.selector = selector

    def register(self, socket, address, read=True, write=True, timeout=60):
        socket.settimeout(timeout)
        socket.setblocking(False)
        events = (selectors.EVENT_READ if read else 0) | (selectors.EVENT_WRITE if write else 0)
        connection = Connection(address)
        data = types.SimpleNamespace(
            connection=connection,
            address=address,
        )
        self.selector.register(socket, events, data=data)
        return connection

    def unregister(self, socket):
        self.selector.unregister(socket)
        socket.close()
        
    def process(self, key, mask):
        socket = key.fileobj
        data = key.data
        stream = data.connection.stream
        if mask & selectors.EVENT_READ:
            if len(stream.read) > 0 and stream.read[len(stream.read) - 1]['length'] > 0:
                received = socket.recv(stream.read[len(stream.read) - 1]['length'])
                stream.read[len(stream.read) - 1]['length'] -= len(received)
                stream.read[len(stream.read) - 1]['message'] += received
                if stream.read[len(stream.read) - 1]['length'] == 0 and 'temp' not in stream.read[len(stream.read) - 1]:
                    value = stream.read.pop()
                    stream.read.append({
                        'message': b'',
                        'length': 8,
                        'temp': True
                    })
                    data.connection.emit(value['message'])
                if not received and stream.read[len(stream.read) - 1]['length'] > 0:
                    value = stream.read.pop()
                    stream.read.append({
                        'message': b'',
                        'length': 8,
                        'temp': True
                    })
                    self.selector.unregister(socket)
                    socket.close()
            elif len(stream.read) > 0 and stream.read[len(stream.read) - 1].get('temp', False):
                value = stream.read.pop()
                stream.read.append({
                    'message': b'',
                    'length': int.from_bytes(value['message'], byteorder='big'),
                })
                self.process(key, selectors.EVENT_READ)
            else:
                stream.read.append({
                    'message': b'',
                    'length': 8,
                    'temp': True
                })
                self.process(key, selectors.EVENT_READ)
        if mask & selectors.EVENT_WRITE:
            if len(stream.messages) > 0 and len(stream.messages[0]['message']) > 0:
                sent = socket.send(stream.messages[0]['message'])
                stream.messages[0]['message'] = stream.messages[0]['message'][sent:]
                if len(stream.messages[0]['message']) == 0:
                    stream.messages.pop(0)
            elif len(stream.messages) > 0:
                stream.messages.pop(0)
                self.process(key, selectors.EVENT_WRITE)

    def step(self):
        events = self.selector.select(timeout=0)
        for key, mask in events:
            self.process(key, mask)
