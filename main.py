import threading

from handler import Handler
from server import Server
from client import Client
#from window import Window

class Main:
    def __init__(self):
        self.handler = Handler()
        self.server = Server(self.handler)
        self.client = Client(self.handler)
        #self.window = Window(self.server, self.client)

        
    def run(self):
        server_thread = threading.Thread(target=self.server.run)
        server_thread.start()

        
        client_thread = threading.Thread(target=self.client.run, args=(input()))
        client_thread.start()

        server_thread.join()


if __name__ == "__main__":
    main = Main()
    main.run()