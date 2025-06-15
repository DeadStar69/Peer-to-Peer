import threading
import sys

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

        while True:
            a = input()
            if a == "exit":
                server_stopping_thread = threading.Thread(target=self.server.stop)
                server_stopping_thread.start()
                sys.exit()

            elif a == "msg":
                b = input()
                threading.Thread(target=self.client.sendMessages, args=(b, )).start()

            else:
                client_thread = threading.Thread(target=self.client.connectTo, args=(a, ))
                client_thread.start()

                client_thread.join()


if __name__ == "__main__":
    main = Main()
    main.run()