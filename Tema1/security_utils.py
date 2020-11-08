import base64
import AES
import random

from enum import IntEnum, unique

def getRandom128():
    return base64.b16encode(random.getrandbits(128).to_bytes(16, byteorder='little')).decode()

def getK3():
    f = open("public_k3.txt", "r").read()
    return f

def getVI():
    f = open("public_VI.txt", "r").read()
    VI_f = [s for s in f]
    return VI_f

@unique
class CipherMode(IntEnum):
    CBC = 1
    OFB = 2

K3 = getK3()
VI = getVI()


