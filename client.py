import socket

from statics import *

class Client:
    def __init__(self, handler):
        self.handler = handler

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectTo(self, ip):
        try:

            self.s.connect((ip, PORT))

            self.handler.client_connections = [self.disassemble_ip_header(self.s.recv(20))][0]
            print(self.handler.client_connections)
            self.s.close()

        except socket.error as e:
            print(e)

                

    def disassemble_ip_header(self, header, size = HEADER_SIZE):
        return [socket.inet_ntoa(header[i*4:i*4+4]) for i in range(size)]
    
                
    def stop(self):
        self.handler.client_running = False
        self.s.close()
        

