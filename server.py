import socket
from statics import *

class Server:
    def __init__(self, handler):
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((SERVER, PORT))

    def run(self):
        
        pass
    
    def stop(self):
        pass