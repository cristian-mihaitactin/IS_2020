from Crypto.Cipher import AES
import random

IV = random.new().read(AES.block_size)

with open("public_VI.txt", "r+") as f:
    data = f.read()
    f.seek(0)
    f.write()
