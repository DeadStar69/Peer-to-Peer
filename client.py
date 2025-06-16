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

            received = self.s.recv(HEADER_SIZE)
            other_connections = self.disassembleInfoHeader(received)

            self.s.send(f"{self.handler.PORT:#<5}".encode())

            self.handler.connections = mergeLists(self.handler.connections, other_connections)

            if [ip, port] not in self.handler.connections:
                self.handler.connections.append([ip, port])

            #print(f"Connected peers: {other_connections}")
            #print(f"Current connections: {self.handler.connections}")

            for other_ip, other_port in other_connections:
                if [other_ip, other_port] not in self.handler.connections:
                    print(f"Connecting to new peer from {ip}:{port} → {other_ip}:{other_port}")
                    self.connectTo(other_ip, other_port)

            self.s.close()

            self.sendMessages(f"joined the network")

        except socket.error as e:
            print("Connection error:", e)

    def sendMessages(self, message: str):
        temp = []

        for ip, port in self.handler.connections[:]:

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((ip, port))

                temp.append([ip, port])

                other_connections = self.disassembleInfoHeader(s.recv(HEADER_SIZE))
                s.send(f"{self.handler.PORT:#<5}".encode())

                self.handler.connections = mergeLists(self.handler.connections, other_connections)

                s.send(f"<MESSAGETRANSFERPROTOCOL>{message:#<{BUFFER - 25}}".encode())
                s.close()

            except socket.error:
                if [ip, port] in self.handler.connections:
                    self.handler.connections.remove([ip, port])


        for connection in self.handler.connections:

            if connection not in temp:
                ip, port = connection

                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(5)
                    s.connect((ip, port))

                    other_connections = self.disassembleInfoHeader(s.recv(HEADER_SIZE))
                    s.send(f"{self.handler.PORT:#<5}".encode())

                    self.handler.connections = mergeLists(self.handler.connections, other_connections)

                    s.send(f"<MESSAGETRANSFERPROTOCOL>{message:#<{BUFFER - 25}}".encode())
                    s.close()

                    temp.append(connection)

                except socket.error:
                    if connection in self.handler.connections:
                        self.handler.connections.remove(connection)

        #print("Final connections:", self.handler.connections)

    def sendFile(self, file_path: str, file_name: str):
        
        for ip, port in self.handler.connections[:]:

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((ip, port))

                other_connections = self.disassembleInfoHeader(s.recv(HEADER_SIZE))
                s.send(f"{port:#<5}".encode())

                self.handler.connections = mergeLists(self.handler.connections, other_connections)

                file_size = os.path.getsize(file_path)

                s.send(f"<FILETRANSFERPROTOCOL>{file_size}{SEPARATOR}{file_name:#<{1024 - len(f'<FILETRANSFERPROTOCOL>{file_size}{SEPARATOR}')}}".encode())

                with open(file_path, "rb") as f:
                    data = f.read(BUFFER)
                    while data and self.handler.client_running:
                        s.send(data)
                        data = f.read(BUFFER)

                s.close()

            except socket.error:
                if [ip, port] in self.handler.connections:
                    self.handler.connections.remove([ip, port])

    def createIpHeader(self, connections, size=HEADER_LENGTH):
        padded_connections = (connections + [["0.0.0.0", 0]] * size)[:size]
        binary_entries = [
            socket.inet_aton(ip) + struct.pack("!H", port)
            for ip, port in padded_connections
        ]
        return b"".join(binary_entries)

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
