import socket

from statics import *

class Client:
    def __init__(self, handler):
        self.handler = handler

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connectTo(self, ip):

        try:
            self.s.connect((ip, PORT))

            self.handler.connections = self.disassembleIpHeader(self.s.recv(20))

            if self.handler.IP not in self.handler.connections: self.handler.connections.append(self.IP)

            self.s.send(ENDMARKER)
                
            print(self.handler.connections)

            self.s.close()

        except socket.error as e:
            print(e)

    def sendMessages(self, message: str):
        
        for ip in self.handler.connections:

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, PORT))

                other_connections = self.disassembleIpHeader(s.recv(20))

                if other_connections != self.handler.connections:
                    self.handler.connections = longerList(other_connections, self.handler.connections)

                total_sent = 0
                data_bytes = message.encode()

                data_bytes = data_bytes + ENDMARKER

                while total_sent < len(data_bytes):

                    sent = s.send(data_bytes[total_sent:])

                    
                    total_sent += sent

                self.s.close()

            except socket.error as e:
                self.handler.connections.remove(ip)

                
    def disassembleIpHeader(self, header, size=HEADER_LENGTH):
        return [socket.inet_ntoa(header[i*4:i*4+4]) for i in range(size) if socket.inet_ntoa(header[i*4:i*4+4]) != "0.0.0.0"]
    
                
    def stop(self):
        self.handler.client_running = False
        self.s.close()
        

