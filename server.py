import socket
from statics import *

class Server:
    def __init__(self, handler):
        self.handler = handler

        self.IP = socket.gethostbyname(socket.gethostname())

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.IP, PORT))
        self.s.listen()
        self.s.settimeout(3)

    def run(self):

        while True:

            if not self.handler.server_running: break

            try:
                conn, addr = self.s.accept()
                print(addr, "mrs")
                print(conn.recv(1024).decode())
                conn.close()
                self.s.close()
                break

            except TimeoutError as e:
                print(e)
                continue

    
    def stop(self):
        self.handler.server_running = False