import socket

from statics import *

class Handler:
    def __init__(self):
        self.IP = socket.gethostbyname(socket.getfqdn())
        self.PORT = PORT
        self.server_running = True
        self.client_running = True
        self.connections = []
        self.connected = []
        self.history = ["akjhsdjajdsav"]