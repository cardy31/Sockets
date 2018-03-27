import socket
import threading


class ThreadedServer:

    # Key/value storage
    dictionary = {}

    def __init__(self, host, port):
        if host is None:
            self.host = socket.gethostname()
        else:
            self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            # Create a new thread for every client
            threading.Thread(target=self.listen_to_client, args=(client,)).start()

    def listen_to_client(self, client):
        size = 1024
        while True:
            try:
                data = client.recv(size).decode()
                if data:
                    request_type = data.split(' ')[0]

                    if request_type == 'set':
                        client.send(self.set(data).encode())
                    elif request_type == 'get':
                        client.send(self.get(data).encode())
                    elif request_type == 'delete':
                        client.send(self.delete(data).encode())
                    elif request_type == 'showall':
                        client.send(self.dictionary.__str__().encode())
                    else:
                        client.send('Incorrect format. Type \'h\' for type'.encode())

                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

    def get(self, data):
        value = self.dictionary.get(data[4:])
        if value is not None:
            return value
        else:
            return 'Could not find an entry for that key'

    def set(self, data):
        key = data.split(':')[0][4:]
        value = data.split(':')
        if len(value) > 1:
            value = value[1]
        else:
            value = None
        if key is not None and value is not None:
            self.dictionary.update({key: value})
            return 'Set new entry\n    key: {}, value: {}'.format(key, value)
        else:
            return 'Must have key and value in set command'

    def delete(self, data):
        key = data[7:]
        if key in self.dictionary:
            self.dictionary.pop(key)
            return 'Deleted {}'.format(key)
        else:
            return 'Could not find an entry for that key'


if __name__ == '__main__':
    port_num = 12345
    hostname = socket.gethostname()
    ThreadedServer(hostname, port_num).listen()
