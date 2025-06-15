import socket

class Handler:
    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.server_running = True
        self.client_running = True
        self.connections = []
