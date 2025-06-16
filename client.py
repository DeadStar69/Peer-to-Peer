import socket
import struct
import os

from statics import *

class Client:
    def __init__(self, handler):
        self.handler = handler

    def connectTo(self, ip, port):

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(5)
            self.s.connect((ip, port))

            self.handler.connections = self.disassembleInfoHeader(self.s.recv(HEADER_SIZE))

            self.s.send(f"{self.handler.PORT:#<5}".encode())

            if port not in [x for y,x in self.handler.connections]: self.handler.connections.append([self.handler.IP, port])

            if self.handler.PORT not in [x for y,x in self.handler.connections]: self.handler.connections.append([self.handler.IP, self.handler.PORT])

            self.sendMessages(f"{[self.handler.IP, self.handler.PORT]} Connected to the network")
                
            print(self.handler.connections)


        except socket.error as e:
            print(e)

    def sendMessages(self, message: str):
        
        for ip, port in self.handler.connections:

            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(5)
                self.s.connect((ip, port))

                other_connections = self.disassembleInfoHeader(self.s.recv(HEADER_SIZE))

                self.s.send(f"{port:#<5}".encode())

                self.handler.connections = mergeLists(other_connections, self.handler.connections)

                self.s.send(f"<MESSAGETRANSFERPROTOCOL>{message:#<{BUFFER-25}}".encode())

                self.s.close()

            except socket.error as e:
                self.handler.connections.remove([ip, port])

    def sendFile(self, file_path: str, file_name: str):
        for ip, port in self.handler.connections:

            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(5)
                self.s.connect((ip, port))

                other_connections = self.disassembleInfoHeader(self.s.recv(HEADER_SIZE))

                self.s.send(f"{port:#<5}".encode())

                if other_connections != self.handler.connections:
                    self.handler.connections = longerList(other_connections, self.handler.connections)

                file_size = os.path.getsize(file_path)

                self.s.send(f"<FILETRANSFERPROTOCOL>{file_size}{SEPARATOR}{file_name:#<{1024 - len(f'<FILETRANSFERPROTOCOL>{file_size}{SEPARATOR}')}}".encode())

                with open(f"{file_path}", "rb") as f:
                    data = f.read(BUFFER)
                    while data:
                        if not self.handler.client_running: break
                        self.s.send(data)
                        data = f.read(BUFFER)
                    f.close()

                self.s.close()

            except socket.error as e:
                self.handler.connections.remove([ip, port])

    def disassembleInfoHeader(self, header, size=HEADER_LENGTH):
        connections = []

        for i in range(size):
            offset = i * 6
            ip_bytes = header[offset:offset+4]
            port_bytes = header[offset+4:offset+6]
            
            ip = socket.inet_ntoa(ip_bytes)
            port = struct.unpack("!H", port_bytes)[0]

            if ip != "0.0.0.0" or port != 0:
                connections.append([ip, port])

        return connections
    
                
    def stop(self):
        self.handler.client_running = False
        self.s.close()
        

