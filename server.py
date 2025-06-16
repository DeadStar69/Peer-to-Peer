import socket
import sys
import os

from statics import *

class Server:
    def __init__(self, handler):
        self.handler = handler

        try:
            os.mkdir("output")
        except FileExistsError:
            pass

        self.handler.connections.append(self.handler.IP)
        self.s = None

    def run(self):

        while True:

            if not self.handler.server_running: break
            
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.handler.IP, PORT))
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

                if received_data.startswith("<FILETRANSFERPROTOCOL>") is True:
                    file_name = received_data.strip("<FILETRANSFERPROTOCOL>")
                    print(file_name)
                    with open(f"output/{file_name}", "wb") as f:
                        data = conn.recv(BUFFER)
                        while data:
                            if not self.handler.client_running:
                                f.close()
                                os.remove(f"output/{file_name}")
                                break
                            else:
                                if data.endswith(ENDMARKER) is True:
                                    f.write(data.rstrip(ENDMARKER))
                                    break
                                f.write(data)
                                data = conn.recv(BUFFER)
                        f.close()
                        print("file received")

                elif received_data.startswith("<MESSAGETRANSFERPROTOCOL>") is True:
                    message = received_data.strip("<MESSAGETRANSFERPROTOCOL>")
                    print(f"{addr}> {message}")


                print(self.handler.connections)
                
                conn.close()

            except socket.timeout:
                continue


    def createIpHeader(self, connections, size=HEADER_LENGTH):
        padded_ips = (connections + ["0.0.0.0"] * size)[:size]
        binary_ips = [socket.inet_aton(ip) for ip in padded_ips]
        return b"".join(binary_ips)

    
    def stop(self):
        self.handler.server_running = False
        self.s.close()