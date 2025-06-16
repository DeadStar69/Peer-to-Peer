import socket
IP = socket.gethostbyname(socket.getfqdn())

print(IP)