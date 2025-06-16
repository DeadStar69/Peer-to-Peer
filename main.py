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
        server_thread = threading.Thread(target=self.server.run, args=(int(input("Enter server port: ")), ), daemon=True)
        server_thread.start()

        while True:
            a = input("> ")

            if not a: continue

            args = a.split(" ")

            if args[0] == "exit":
                threading.Thread(target=self.server.stop).start()
                sys.exit()

            elif args[0] == "msg":
                threading.Thread(target=self.client.sendMessages, args=(args[1], ), daemon=True).start()

            elif args[0] == "file":
                threading.Thread(target=self.client.sendFile, args=(args[1], args[2], ), daemon=True).start()

            elif args[0] == "connect":
                client_thread = threading.Thread(target=self.client.connectTo, args=(args[1], int(args[2]), ), daemon=True)
                client_thread.start()

            elif args[0] == "stop":
                threading.Thread(target=self.client.stop, daemon=True).start()


if __name__ == "__main__":
    main = Main()
    main.run()