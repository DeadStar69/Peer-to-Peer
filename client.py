import socket

from statics import PORT

class Client:
    def __init__(self, handler):
        self.handler = handler

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.s.connect((socket.gethostbyname(socket.gethostname()), PORT))
        self.s.send("retard".encode())
        self.stop
        

    def stop(self):
        self.handler.client_running = False
        self.s.close()

