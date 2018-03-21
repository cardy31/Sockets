import socket
from time import sleep


def main():
    Client()


class Client:

    def __init__(self):
        print("Welcome to this simple redis-like application. This acts as a key/value store on a server.")
        print("Type 'h' for help")

        sock = None
        print("\nEstablishing connection...")
        while sock is None:
            sock = self.start_client()
        print("Connection established.")
        self.listen(sock)

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

    def listen(self, sock):
        while True:
            text = input("> ")
            if text == 'h':
                self.print_help()
            elif text == '':
                pass
            else:
                if text.__sizeof__() > 1024:
                    print("Total size of input cannot be greater than 1024 bytes.")
                else:
                    sock.send(text.encode())
                    print(sock.recv(1024).decode())

    @staticmethod
    def print_help():
        print("Help Menu")
        print("Add a value to the dictionary:\n"
              "    set <key>:<value>")
        print("Retrieve a value from the dictionary:\n"
              "    get <key>")
        print("Delete a value from the dictionary:\n"
              "    delete <key>")
        print("See all values in the dictionary:\n"
              "    showall")
        print("Please note that values stored by one user can by accessed by any other user.")


main()
