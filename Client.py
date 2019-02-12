import socket
from time import sleep


class Client:

    sock = None

    def __init__(self):
        sock = None
        print('\nEstablishing connection...')
        while sock is None:
            sock = self.start_client()
        print('Connection established\n')
        self.run = True
        self.sock = sock
        # Welcome message
        print('Welcome to this simple redis-like application. This acts as a key/value store on a server.')
        print('Type \'h\' for help')

    @staticmethod
    def start_client():
        sock = socket.socket()
        host = socket.gethostname()
        port = 12345
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            print("Connection refused. The server may be down. Retrying in 5 seconds.")
            sleep(5)
            return None
        return sock

    '''
    Added to make testing easier
    '''
    def listen_driver(self):
        while self.run:
            output = self.listen()
            if output is not None:
                print(output)
        self.cleanup()

    def listen(self):
        text = input('> ')
        if text == 'h':
            return self.print_help()
        elif text == '':
            return None
        elif text == 'exit':
            self.run = False
            return 'Goodbye :-)'
        else:
            if text.__sizeof__() > 1024:
                return "Total size of input cannot be greater than 1024 bytes."
            else:
                self.sock.send(text.encode())
                data = self.sock.recv(1024).decode()
                return data

    @staticmethod
    def print_help():
        return "Help Menu\n" + \
            "Add a value to the dictionary:\n" \
            "    set <key>:<value>\n" \
            "Retrieve a value from the dictionary:\n" \
            "    get <key>\n" \
            "Delete a value from the dictionary:\n" \
            "     delete <key>\n" + \
            "See all values in the dictionary:\n" \
            "    showall\n" \
            "Please note that values stored by one user can by accessed by any other user."

    def cleanup(self):
        self.sock.close()


if __name__ == "__main__":
    Client().listen_driver()
