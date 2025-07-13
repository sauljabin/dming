message = "WLMW WL EA EWFLSBW"
characters = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


def get_by_offset(char, offset):
    char_index = characters.index(char)
    position = (char_index + offset) % len(characters)
    return characters[position]


def decrypt(message, offset):
    for c in message:
        yield get_by_offset(c, offset) if c in characters else c


interval = 27

for i in range(-interval, interval + 1):
    print(f"offset: {i:3}, message: {"".join(decrypt(message, i))}")
