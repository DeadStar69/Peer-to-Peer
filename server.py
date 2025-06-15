import socket
from statics import *

class Server:
    def __init__(self, handler):
        self.handler = handler

        self.IP = socket.gethostbyname(socket.gethostname())

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.IP, PORT))
        self.s.listen()

    def run(self):

        while True:

            if not self.handler.server_running: break

            conn, addr = self.s.accept()
            print(conn.recv(1024).decode())
            conn.close()
            self.stop()

                





    
    def stop(self):
        self.handler.server_running = False