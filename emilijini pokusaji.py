import socket
import threading

PORT = 13228
SERVER = socket.gethostbyname(socket.gethostname()) #ovo ce mi dati moji lokalnu ip adresu
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) 

def handle_client(addr, conn):
    print("[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg = conn.recv()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()