import socket
import json
import os
from datetime import datetime
from statics import *

class Client:
    def __init__(self, handler):
        self.handler = handler

    def connectTo(self, ip, port):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((ip, port))

            other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE))
            history_size = int(s.recv(20).decode().rstrip("#"))
            other_history = json.loads(s.recv(history_size).decode())
            
            self.handler.connections = mergeLists(self.handler.connections, other_connections)
            self.handler.history = mergeHistories(self.handler.history, other_history)

            s.send(f"{self.handler.PORT:#<5}".encode())
            
            if [ip, port] not in self.handler.connections:
                self.handler.connections.append([ip, port])

            for other_ip, other_port in other_connections:
                if [other_ip, other_port] not in self.handler.connections:
                    print(f"Connecting to new peer from {ip}:{port} → {other_ip}:{other_port}")
                    self.connectTo(other_ip, other_port)

            s.close()

            self.sendMessages(f"joined the network")

        except json.decoder.JSONDecodeError:
            pass

        except TypeError:
            pass

        except socket.error as e:
            print("Connection error:", e)

    def sendMessages(self, message: str):
        temp = []

        for ip, port in self.handler.connections[:]:
            if (ip, port) == (self.handler.IP, self.handler.PORT):
                continue

            try:
                self.Mica(ip, port, message)

                temp.append([ip, port])


            except json.decoder.JSONDecodeError:
                pass

            except TypeError:
                pass

            except socket.error:
                if [ip, port] in self.handler.connections:
                    self.handler.connections.remove([ip, port])


        for connection in self.handler.connections:

            if connection not in temp:
                ip, port = connection
                if (ip, port) == (self.handler.IP, self.handler.PORT):
                    continue

                try:
                    self.Mica(ip, port, message)
                
                    temp.append(connection)

                except json.decoder.JSONDecoder:
                    pass

                except TypeError:
                    pass

                except socket.error:
                    if connection in self.handler.connections:
                        self.handler.connections.remove(connection)

        self.handler.history[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = f"{self.handler.IP}, {self.handler.PORT}> {message}"
        os.system('cls')
        for timestamp in sorted(self.handler.history):
            print(f"[{timestamp}] {self.handler.history[timestamp]}")

        print("> ", end="", flush=True)
    
    def Mica(self, ip, port, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, port)) # 1

        other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE)) # 2

        history_size = int(s.recv(20).decode().rstrip("#")) # 3
        other_history = json.loads(s.recv(history_size).decode()) # 3

        self.handler.connections = mergeLists(self.handler.connections, other_connections) # merge 2
        self.handler.history = mergeHistories(self.handler.history, other_history) # merge 3 i 4

        history_temp = json.dumps(self.handler.history).encode()
        s.send(f"{len(history_temp):#<20}".encode()) # 4
        s.send(history_temp) # 4

        s.send(f"{self.handler.PORT:#<5}".encode()) # 5

        s.send(f"<MESSAGETRANSFERPROTOCOL>{message:#<{BUFFER - 25}}".encode()) # 6
        
        s.close()


    # def sendFile(self, file_path: str, file_name: str):
        
    #     for ip, port in self.handler.connections[:]:

    #         try:
    #             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             s.settimeout(5)
    #             s.connect((ip, port))

    #             other_connections = disassembleInfoHeader(s.recv(HEADER_SIZE))

    #             s.send(f"{port:#<5}".encode())

    #             self.handler.connections = mergeLists(self.handler.connections, other_connections)


    #             file_size = os.path.getsize(file_path)

    #             s.send(f"<FILETRANSFERPROTOCOL>{file_size}{SEPARATOR}{file_name:#<{1024 - len(f'<FILETRANSFERPROTOCOL>{file_size}{SEPARATOR}')}}".encode())

    #             with open(file_path, "rb") as f:
    #                 data = f.read(BUFFER)
    #                 while data and self.handler.client_running:
    #                     s.send(data)
    #                     data = f.read(BUFFER)

    #             s.close()

    #         except socket.error:
    #             if [ip, port] in self.handler.connections:
    #                 self.handler.connections.remove([ip, port])


    def stop(self):
        self.handler.client_running = False
