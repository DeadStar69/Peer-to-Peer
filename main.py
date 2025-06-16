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
        server_thread = threading.Thread(target=self.server.run, daemon=True)
        server_thread.start()

        while True:
            a = input()

            if not a: continue

            a = a.split(" ")

            if a[0] == "exit":
                threading.Thread(target=self.server.stop).start()
                sys.exit()

            elif a[0] == "msg":
                a.pop(0)
                threading.Thread(target=self.client.sendMessages, args=(" ".join(a), ), daemon=True).start()

            elif a[0] == "file":
                a.pop(0)
                threading.Thread(target=self.client.sendFile, args=(a[0], a[1], ), daemon=True).start()

            elif a[0] == "connect":
                client_thread = threading.Thread(target=self.client.connectTo, args=(a[1], ), daemon=True)
                client_thread.start()

            elif a[0] == "stop":
                threading.Thread(target=self.client.stop, daemon=True).start()


if __name__ == "__main__":
    main = Main()
    main.run()