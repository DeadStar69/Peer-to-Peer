import socket
import struct
import sys
import os

from statics import *

class Server:
    def __init__(self, handler, ):
        self.handler = handler

        try:
            os.mkdir("output")
        except FileExistsError:
            pass

        self.s = None

    def run(self, port):
        self.handler.connections.append([self.handler.IP, port])
        while True:

            if not self.handler.server_running: break
            
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.handler.IP, port))
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

                received_data = conn.recv(BUFFER).decode().rstrip("#")

                if received_data.startswith("<FILETRANSFERPROTOCOL>"):
                    received_data = received_data[len("<FILETRANSFERPROTOCOL>"):]
                    file_size_str, file_name = received_data.split(SEPARATOR)
                    file_size = int(file_size_str)
                    
                    with open(f"output/{file_name}", "wb") as f:
                        received_bytes = 0
                        while received_bytes < file_size:
                            if not self.handler.client_running:
                                f.close()
                                os.remove(f"output/{file_name}")
                                break
                            data = conn.recv(min(BUFFER, file_size - received_bytes))
                            if not data:
                                break
                            f.write(data)
                            received_bytes += len(data)
                        
                        if received_bytes == file_size:
                            print(f"File {file_name} received successfully")
                        else:
                            print("File received unsuccesfully")

                elif received_data.startswith("<MESSAGETRANSFERPROTOCOL>") is True:
                    received_data[len("<MESSAGETRANSFERPROTOCOL>"):]
                    message = received_data[len("<MESSAGETRANSFERPROTOCOL>"):]
                    print(f"{addr}> {message}")


                print(self.handler.connections)
                
                conn.close()

            except socket.timeout:
                continue


    def createIpHeader(self, connections, size=HEADER_LENGTH):
        padded_connections = (connections + [["0.0.0.0", 0]] * size)[:size]
        binary_entries = [
            socket.inet_aton(ip) + struct.pack("!H", port)
            for ip, port in padded_connections
        ]
        return b"".join(binary_entries)

    
    def stop(self):
        self.handler.server_running = False
        self.s.close()