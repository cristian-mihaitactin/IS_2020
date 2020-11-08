import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

import random

from enum import IntEnum, unique

def getRandom128():
    return base64.b16encode(random.getrandbits(128).to_bytes(16, byteorder='little')).decode()
    #return hashlib.sha256(bs64.encode('utf-8')).digest()
    #return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()

def getK3():
    f = open("public_k3.txt", "r").read()
    return f

def getVI():
    with open("public_VI.txt", "rb") as f:
        data = f.read()
        print('IV:',data)
        return data

def hashKey(plain_key):
    return hashlib.sha256(plain_key.encode()).digest()

def AES_encrypt_singleblock(plain):
    hash_key = hashKey(K3)
    cipher = AES.new(hash_key, AES.MODE_CBC, VI)
    plain = _pad(plain)

    return base64.b64encode(VI + cipher.encrypt(plain.encode()))

def AES_dencrypt_singleblock(encrypted):
    encrypted = base64.b64decode(encrypted)
    iv = encrypted[:AES.block_size]
    cipher = AES.new(hashKey(K3), AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(encrypted[AES.block_size:])).decode('utf-8')

def _pad(st):
        return st + (AES.block_size - len(st) % AES.block_size) * chr(AES.block_size - len(st) % AES.block_size)

def _unpad(st):
        return st[:-ord(st[len(st)-1:])]
@unique
class CipherMode(IntEnum):
    CBC = 1
    OFB = 2

K3 = getK3()
VI = getVI()

def ecrypt_CBC(key,msg):
    hashkey = hashKey(key)
    cipher = AES.new(hashkey, AES.MODE_CBC, VI)
    print (msg.encode())
    print (len(msg.encode()))
    if (len(msg.encode()) % 16 != 0):
        msg = _pad(msg)

    return base64.b64encode(VI + cipher.encrypt(msg.encode()))

def decrypt__CBC(key,encr_msg):
    hashkey = hashKey(key)
    encr_msg = base64.b64decode(encr_msg)
    iv = encr_msg[:AES.block_size]
    cipher = AES.new(hashkey, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(encr_msg[AES.block_size:])).decode('utf-8')
    #return cipher.decrypt(encr_msg[AES.block_size:]).decode('utf-8')

def ecrypt_OFB(key,msg):
    raise Exception("Not Implemented!")

def ecryptMessage(cipher_mode:CipherMode, key, msg):
    if (cipher_mode == CipherMode.CBC):
        return ecrypt_CBC(key,msg)
    elif(cipher_mode == CipherMode.OFB):
        return ecrypt_OFB(key,msg)
    else:
        return 'Unsupported cipher mode'