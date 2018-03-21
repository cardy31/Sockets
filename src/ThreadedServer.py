import socket
import threading


def main():
    port_num = 12345
    ThreadedServer('', port_num).listen()


class ThreadedServer:

    dictionary = {}

    def __init__(self, host, port):
        if host is None:
            self.host = socket.gethostname()
        else:
            self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind(('', self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size).decode()
                if data:
                    type = data.split(' ')[0]

                    if type == 'set':
                        client.send(self.set(data).encode())
                    elif type == 'get':
                        client.send(self.get(data).encode())
                    elif type == 'delete':
                        client.send(self.delete(data).encode())
                    elif type == 'showall':
                        client.send(self.dictionary.__str__().encode())
                    else:
                        client.send('Incorrect format. Must be <get/set> <key>:<(if get)value>'.encode())

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
            return "Could not find a value for that key"

    def set(self, data):
        key = data.split(':')[0][4:]
        value = data.split(':')[1]
        if key is not None and value is not None:
            self.dictionary.update({key: value})
        else:
            return "Must have key and value in set command"
        return "Set new entry\n    key: {}, value: {}".format(key, value)

    def delete(self, data):
        key = data[7:]
        if key in self.dictionary:
            self.dictionary.pop(key)
            return "Deleted {}".format(key)
        else:
            return "Could not find an entry for that key"


main()
