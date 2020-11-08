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

def ecrypt_CBC(key,plain_text):
    hashkey = hashKey(key)
    cipher = AES.new(hashkey, AES.MODE_CBC, VI)
    print (plain_text.encode())
    print (len(plain_text.encode()))
    if (len(plain_text.encode()) % 16 != 0):
        plain_text = _pad(plain_text)

    return base64.b64encode(VI + cipher.encrypt(plain_text.encode()))

def decrypt_CBC(key,encr_msg):
    hashkey = hashKey(key)
    encr_msg = base64.b64decode(encr_msg)
    iv = encr_msg[:AES.block_size]
    cipher = AES.new(hashkey, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(encr_msg[AES.block_size:])).decode('utf-8')
    #return cipher.decrypt(encr_msg[AES.block_size:]).decode('utf-8')

def ecrypt_OFB(key,plain_text):
    pos = 0
    cipherTextChunks = []
    ocb_iv = VI
    #originalIV = VI
    key = hashKey(key)
    cipher = AES.new(key, AES.MODE_ECB)
    if (len(plain_text.encode()) % 16 != 0):
        plain_text = _pad(plain_text)
    # ?
    plain_text = plain_text.encode()
    # ?
    while pos + 16 <= len(plain_text):
        toXor = cipher.encrypt(VI)
        nextPos = pos + 16
        toEnc = plain_text[pos:nextPos]
        cipherText = bytes([toXor[i] ^ toEnc[i] for i in range(16)])
        cipherTextChunks.append(cipherText)
        pos += 16
        ocb_iv = toXor
    return cipherTextChunks

def decrypt_OFB(key,encr_msg):
    plainText = b""
    key = hashKey(key)
    iv = VI
    print('type(encr_msg)', type(encr_msg))
    print('encr_msg', encr_msg)
    cipher = AES.new(key, AES.MODE_ECB)
    for chunk in encr_msg:
        toXor = cipher.encrypt(VI)
        plainText += bytes([toXor[i] ^ chunk[i] for i in range(15)])
        iv = toXor
    while plainText[-1] == 48:
        plainText = plainText[0:-1]
    if plainText[-1] == 49:
        plainText = plainText[0:-1]
    return plainText

def ecryptMessage(cipher_mode:CipherMode, key, msg):
    if (cipher_mode == CipherMode.CBC):
        return ecrypt_CBC(key,msg)
    elif(cipher_mode == CipherMode.OFB):
        return ecrypt_OFB(key,msg)
    else:
        return 'Unsupported cipher mode'

def decryptMessage(cipher_mode:CipherMode, key, encr_msg):
    if (cipher_mode == CipherMode.CBC):
        return decrypt_CBC(key,encr_msg)
    elif(cipher_mode == CipherMode.OFB):
        return decrypt_OFB(key,encr_msg)
    else:
        return 'Unsupported cipher mode'