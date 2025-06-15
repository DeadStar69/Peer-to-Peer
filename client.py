import socket

from statics import PORT

class Client:
    def __init__(self, handler):
        self.handler = handler

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, addr):
        self.s.connect((addr, PORT))
        self.s.send("retard".encode())
        self.s.close()
        print("poslato")

    def stop(self):
        self.handler.client_running = False
        

