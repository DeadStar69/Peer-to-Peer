import struct
import socket

PORT = 13229
HEADER_LENGTH = 10
HEADER_SIZE = HEADER_LENGTH * 6
BUFFER = 1024
HISTORY_SIZE = BUFFER * HEADER_LENGTH
SEPARATOR = "<SEPARATOR>"


def mergeLists(list1, list2):
    return list1 + [item for item in list2 if item not in list1]

def mergeHistories(h1, h2):
    combined = {**h2, **h1}
    result = {}
    seen_values = set()

    for k, v in sorted(combined.items()):
        if v not in seen_values:
            result[k] = v
            seen_values.add(v)

    return result

def createIpHeader(connections, size=HEADER_LENGTH):
    padded_connections = (connections + [["0.0.0.0", 0]] * size)[:size]
    binary_entries = [socket.inet_aton(ip) + struct.pack("!H", port) for ip, port in padded_connections]
    return b"".join(binary_entries)

def disassembleInfoHeader(header, size=HEADER_LENGTH):
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
