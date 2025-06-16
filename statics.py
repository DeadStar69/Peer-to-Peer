PORT = 13229
HEADER_LENGTH = 5
HEADER_SIZE = HEADER_LENGTH * 6
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"


def mergeLists(list1, list2):
    return list1 + [item for item in list2 if item not in list1]
