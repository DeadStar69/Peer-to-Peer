import socket
import sys

from statics import *

class Server:
    def __init__(self, handler):
        self.handler = handler

        try:

            self.IP = socket.gethostbyname(socket.gethostname())
            self.handler.server_connections.append(self.IP)

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.IP, PORT))
            self.s.listen()
            self.s.settimeout(1)

        except socket.error as e:
            print(e)
            sys.exit()

    def run(self):

        while True:

            if not self.handler.server_running: break

            try:
                conn, addr = self.s.accept()
                print(addr, "CONNECTED")
                print(self.handler.server_connections)
                conn.send(self.create_ip_header(self.handler.server_connections))
                self.handler.server_connections.append(addr[0])
                conn.close()
                self.s.close()

            except TimeoutError as e:
                continue

            else:
                conn.close()
                self.s.close()
                break

    def create_ip_header(self, connections, size=HEADER_SIZE):
        padded_ips = (connections + ["0.0.0.0"] * size)[:size]
        binary_ips = [socket.inet_aton(ip) for ip in padded_ips]
        return b"".join(binary_ips)


    
    def stop(self):
        self.handler.server_running = False
        self.s.close()