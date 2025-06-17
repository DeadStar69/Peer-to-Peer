import socket
import sys
import os
import threading
import json
from datetime import datetime

from statics import *

class Server:
    def __init__(self, handler, port):
        self.handler = handler
        self.handler.PORT = port

        try:
            os.mkdir("output")
        except FileExistsError:
            pass

        self.s = None

    def run(self):
        self.handler.connections.append([self.handler.IP, self.handler.PORT])

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.handler.IP, self.handler.PORT))
            self.s.listen()
            self.s.settimeout(1)

        except socket.error as e:
            print(e)
            sys.exit()

        while self.handler.server_running:

            try:
                conn, addr = self.s.accept() # 1
                self.handler.connected.append(conn)
                threading.Thread(target=self.receive, args=(conn, addr), daemon=True).start()

            except socket.timeout:
                continue

    def receive(self, conn, addr):

        try:
            conn.send(createIpHeader(self.handler.connections)) # 2
            
            history_temp = json.dumps(self.handler.history).encode()
            conn.send(f"{len(history_temp):#<20}".encode()) # 3
            conn.send(history_temp) # 3

            history_size = int(conn.recv(20).decode().rstrip("#")) # 4
            other_history = json.loads(conn.recv(history_size).decode())
            self.handler.history = mergeHistories(self.handler.history, other_history) # merge 3 i 4
            
            client_port = int(conn.recv(5).decode().rstrip("#")) # 5
            client_info = [addr[0], client_port]

            if client_info not in self.handler.connections:
                self.handler.connections.append(client_info)

            received_data = conn.recv(BUFFER).decode().rstrip("#") # 6

            # if received_data.startswith("<FILETRANSFERPROTOCOL>"):
            #     received_data = received_data[len("<FILETRANSFERPROTOCOL>") :]
            #     file_size_str, file_name = received_data.split(SEPARATOR)
            #     file_size = int(file_size_str)

            #     with open(f"output/{file_name}", "wb") as f:
            #         received_bytes = 0
            #         while received_bytes < file_size and self.handler.client_running:
            #             data = conn.recv(min(BUFFER, file_size - received_bytes))
            #             if not data:
            #                 break
            #             f.write(data)
            #             received_bytes += len(data)
            #     print(f"File {file_name} received successfully" if received_bytes == file_size else "File received unsuccessfully")

            if received_data.startswith("<MESSAGETRANSFERPROTOCOL>"):
                message = received_data[len("<MESSAGETRANSFERPROTOCOL>") :]

                self.handler.history[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = f"{addr[0]}, {client_port}> {message}"

            os.system('cls')
            for timestamp in sorted(self.handler.history):
                print(f"[{timestamp}] {self.handler.history[timestamp]}")

            print("> ", end="", flush=True)

        except json.decoder.JSONDecodeError:
            pass

        except TypeError:
            pass

        except socket.error as e:
            print("SERVER")
            print(e)

    def stop(self):
        self.handler.server_running = False
        for conn in self.handler.connected:
            conn.close()
        self.s.close()
