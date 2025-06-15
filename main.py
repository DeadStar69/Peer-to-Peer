import threading

from handler import Handler
from server import Server
from client import Client
from window import Window

class Main:
    def __init__(self):
        self.handler = Handler()
        self.server = Server(self.handler)
        self.client = Client(self.handler)
        self.window = Window(self.server, self.client)
        
    def run(self):
        pass

if __name__ == "__main__":
    main = Main()
    main.run()