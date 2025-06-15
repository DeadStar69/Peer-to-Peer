import socket
import sys

from statics import *

class Server:
    def __init__(self, handler):
        self.handler = handler

        self.handler.connections.append(self.handler.IP)
        self.s = None

    def run(self):

        while True:

            if not self.handler.server_running: break
            
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.handler.IP, PORT))
                self.s.listen()
                self.s.settimeout(1)

            except socket.error as e:
                print(e)
                sys.exit()


            try:
                conn, addr = self.s.accept()
                print(addr, "CONNECTED")

                conn.send(self.createIpHeader(self.handler.connections))

                if addr[0] not in self.handler.connections: self.handler.connections.append(addr[0])

                raw_message = b""
                
                while True:
                    data = conn.recv(BUFFER)

                    if not data:
                        break

                    raw_message += data

                    if ENDMARKER in raw_message:
                        break

                message = raw_message.split(ENDMARKER)[0].decode()

                print(self.handler.connections)
                print(message)
                conn.close()

            except socket.timeout:
                continue


    def createIpHeader(self, connections, size=HEADER_LENGTH):
        padded_ips = (connections + ["0.0.0.0"] * size)[:size]
        binary_ips = [socket.inet_aton(ip) for ip in padded_ips]
        return b"".join(binary_ips)

    
    def stop(self):
        self.handler.server_running = False
        self.s.close()