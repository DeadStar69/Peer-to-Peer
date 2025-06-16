PORT = 13229
HEADER_LENGTH = 5
HEADER_SIZE = HEADER_LENGTH * 4
BUFFER = 1024
ENDMARKER = "<ENDMARKERRETARD>".encode()

def longerList(list1, list2):
    return list1 if len(list1) >= len(list2) else list2
