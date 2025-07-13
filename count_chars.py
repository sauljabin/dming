message = "Z EVXVH WZI FN HZOGL SZXRZ ZWVOZNGV HRTNRURXZ... WVQZI ZOTFNZH XLHZH ZGIZH"
characters = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


def count_characters(message):
    for c in characters:
        yield f"char: {c}, total: {message.count(c)}"


for string in count_characters(message):
    print(string)
