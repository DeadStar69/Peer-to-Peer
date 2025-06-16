import socket
import struct
import sys
import os
import threading

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
                conn, addr = self.s.accept()
                self.handler.connected.append(conn)
                threading.Thread(target=self.receive, args=(conn, addr), daemon=True).start()

            except socket.timeout:
                continue

    def receive(self, conn, addr):
        
        try:
            conn.send(self.createIpHeader(self.handler.connections))
            client_port = int(conn.recv(5).decode().rstrip("#"))
            client_info = [addr[0], client_port]

            if client_info not in self.handler.connections:
                self.handler.connections.append(client_info)

            received_data = conn.recv(BUFFER).decode().rstrip("#")

            if received_data.startswith("<FILETRANSFERPROTOCOL>"):
                received_data = received_data[len("<FILETRANSFERPROTOCOL>") :]
                file_size_str, file_name = received_data.split(SEPARATOR)
                file_size = int(file_size_str)

                with open(f"output/{file_name}", "wb") as f:
                    received_bytes = 0
                    while received_bytes < file_size and self.handler.client_running:
                        data = conn.recv(min(BUFFER, file_size - received_bytes))
                        if not data:
                            break
                        f.write(data)
                        received_bytes += len(data)
                print(f"File {file_name} received successfully" if received_bytes == file_size else "File received unsuccessfully")

            elif received_data.startswith("<MESSAGETRANSFERPROTOCOL>"):
                message = received_data[len("<MESSAGETRANSFERPROTOCOL>") :]

                print(f"{addr[0]}> {message}")

            print("Current connections:", self.handler.connections)

        except socket.error as e:
            print(e)

    def createIpHeader(self, connections, size=HEADER_LENGTH):
        padded_connections = (connections + [["0.0.0.0", 0]] * size)[:size]
        binary_entries = [socket.inet_aton(ip) + struct.pack("!H", port) for ip, port in padded_connections]
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
        self.handler.server_running = False
        self.s.close()
