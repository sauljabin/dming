message = "Z EVXVH WZI FN HZOGL SZXRZ ZWVOZNGV HRTNRURXZ... WVQZI ZOTFNZH XLHZH ZGIZH"

alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
mirror = ''.join(reversed(alphabet))
equivalences = dict(zip(alphabet, mirror))


def decrypt(message):
    for c in message:
        yield equivalences[c] if c in equivalences else c


print("".join(decrypt(message)))
