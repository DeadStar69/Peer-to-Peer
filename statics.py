PORT = 13229
HEADER_LENGTH = 5
HEADER_SIZE = HEADER_LENGTH * 6
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"

def longerList(list1, list2):
    return list1 if len(list1) >= len(list2) else list2
