import socket
from statics import *

class Server:
    def __init__(self, handler):
        self.handler = handler

        self.IP = socket.gethostbyname(socket.gethostname())
        self.handler.connections.append(self.IP)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.IP, PORT))
        self.s.listen()
        self.s.settimeout(1)

    def run(self):

        while True:

            if not self.handler.server_running: break

            try:
                conn, addr = self.s.accept()
                print(addr, " CONNECTED")
                print(conn.recv(1024).decode())
                conn.close()

            except TimeoutError as e:
                continue

            else:
                conn.close()
                self.s.close()
                break


    
    def stop(self):
        self.handler.server_running = False
        self.s.close()