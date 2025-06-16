PORT = 13229
HEADER_LENGTH = 10
HEADER_SIZE = HEADER_LENGTH * 6
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"

def mergeLists(list1, list2):
    merged = list1[:]
    for item in list2:
        if item not in merged:
            merged.append(item)
    return merged
