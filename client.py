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

            self.handler.connections = self.disassembleInfoHeader(self.s.recv(20))

            if self.handler.IP not in self.handler.connections: self.handler.connections.append(self.handler.IP)
                
            print(self.handler.connections)

            self.s.close()

        except socket.error as e:
            print(e)

    def sendMessages(self, message: str):
        
        for ip in self.handler.connections:

            if ip == self.handler.IP: return

            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(5)
                self.s.connect((ip, PORT))

                other_connections = self.disassembleInfoHeader(self.s.recv(20))

                if other_connections != self.handler.connections:
                    self.handler.connections = longerList(other_connections, self.handler.connections)

                self.s.send(f"<MESSAGETRANSFERPROTOCOL>{message:#<{BUFFER-25}}".encode())

                self.s.close()

            except socket.error as e:
                self.handler.connections.remove(ip)

    def sendFile(self, file_path: str, file_name: str):
        for ip in self.handler.connections:

            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(5)
                self.s.connect((ip, PORT))

                other_connections = self.disassembleInfoHeader(self.s.recv(20))

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
                self.handler.connections.remove(ip)

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
        

