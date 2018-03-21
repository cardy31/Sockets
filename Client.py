import socket


def main():
    Client()


class Client:

    def __init__(self):
        print("Welcome to this simple redis-like program. This acts as a key/value store on a server.")
        print("Type 'h' for help")

        sock = self.start_client()
        self.listen(sock)

    @staticmethod
    def start_client():
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.connect((host, port))

        return s

    def listen(self, sock):
        while True:
            text = input("> ")
            if text == 'h':
                self.print_help()
            elif text == '':
                continue
            else:
                if text.__sizeof__() > 1024:
                    print("Total size of input cannot be greater than 1024 bytes")
                    continue
                sock.send(text.encode())
                print(sock.recv(1024).decode())

    @staticmethod
    def print_help():
        print("Help Menu")
        print("Add a value to the dictionary:\n"
              "    set <key>:<value>")
        print("\nGet a value from the dictionary:\n"
              "    get <key>")


main()
