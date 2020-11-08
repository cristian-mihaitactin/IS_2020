from Crypto.Cipher import AES
from Crypto import Random

IV = Random.new().read(AES.block_size)
print(IV)
#print(IV.decode('unicode_escape'))
print(list(IV))
print('IV Decode:', IV.decode('unicode_escape'))
IV_bytearray = bytearray(IV)

with open("public_VI.txt", "wb+") as f:
    data = f.read()
    f.seek(0)
    f.write(IV_bytearray)
