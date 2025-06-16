import socket
import json
import os
from statics import *

class Client:
    def __init__(self, handler):
        self.handler = handler

    def connectTo(self, ip, port):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            print(ip, port)
            s.connect((ip, port))

            other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE))
            history_size = int(s.recv(20).decode().rstrip("#"))
            other_history = json.loads(s.recv(history_size).decode())

            print(history_size)

            s.send(f"{self.handler.PORT:#<5}".encode())

            self.handler.connections = mergeLists(self.handler.connections, other_connections)
            self.handler.history = mergeLists(self.handler.history, other_history)

            print(self.handler.history)

            if [ip, port] not in self.handler.connections:
                self.handler.connections.append([ip, port])

            #print(f"Connected peers: {other_connections}")
            #print(f"Current connections: {self.handler.connections}")

            for other_ip, other_port in other_connections:
                if [other_ip, other_port] not in self.handler.connections:
                    print(f"Connecting to new peer from {ip}:{port} → {other_ip}:{other_port}")
                    self.connectTo(other_ip, other_port)

            s.close()

            [print(x) for x in self.handler.history]
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

                other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE))
                history_size = int(s.recv(20).decode().rstrip("#"))
                other_history = json.loads(s.recv(history_size).decode())

                s.send(f"{self.handler.PORT:#<5}".encode())

                self.handler.connections = mergeLists(self.handler.connections, other_connections)
                self.handler.history = mergeLists(self.handler.history, other_history)

                print(self.handler.history)

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

                    other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE))
                    history_size = int(s.recv(20).decode().rstrip("#"))
                    other_history = json.loads(s.recv(history_size).decode())

                    s.send(f"{self.handler.PORT:#<5}".encode())

                    self.handler.connections = mergeLists(self.handler.connections, other_connections)
                    self.handler.history = mergeLists(self.handler.history, other_history)

                    s.send(f"<MESSAGETRANSFERPROTOCOL>{message:#<{BUFFER - 25}}".encode())
                    s.close()

                    temp.append(connection)

                except socket.error:
                    if connection in self.handler.connections:
                        self.handler.connections.remove(connection)

        #print("Final connections:", self.handler.connections)
        self.handler.history.append(f"{self.handler.IP}> {message}")

    def sendFile(self, file_path: str, file_name: str):
        
        for ip, port in self.handler.connections[:]:

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((ip, port))

                other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE))
                # history_size = int(s.recv(20).decode().rstrip("#"))
                # other_history = json.loads(s.recv(history_size).decode())

                s.send(f"{port:#<5}".encode())

                self.handler.connections = mergeLists(self.handler.connections, other_connections)
                # self.handler.history = mergeLists(self.handler.history, other_history)


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


    def stop(self):
        self.handler.client_running = False
