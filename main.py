from handler import Handler
from server import Server
from client import Client
class Main:
    def __init__(self):
        self.handler = Handler()
        self.server = Server(self.handler)
        self.client = Client(self.handler)
        
    def run():
        pass

if __name__ == "__main__":
    main = Main()
    main.run()