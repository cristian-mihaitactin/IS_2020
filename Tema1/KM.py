import socket
import curses

import base64
import hashlib

import security_utils
from security_utils import CipherMode

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT_KM = 5001       # The port used by KM

K1 = security_utils.getRandom128()
K2 = security_utils.getRandom128()

print('K1:', K1)
print('K2:', K2)

def CBC():
    print('CBC')
    return K1

def OFB():
    print('OFB')
    return K2

switcher = {
    CipherMode.CBC: CBC,
    CipherMode.OFB: OFB
}

def CipherMode_switcher(argument):
    func = switcher.get(argument, lambda: "Invalid Cipher")
    return func()

def hashLey(plain_key):
    return hashlib.sha256(plain_key.encode()).digest()

def getKey(cipher_mode):
    plain_key = CipherMode_switcher(cipher_mode)


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_KM))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                #print('KM Received', repr(data))
                print('KM Received', data.decode('utf-8'))

                try:
                    cipher_mode = CipherMode(int(data.decode('utf-8')))
                except ValueError as valerr:
                    print('Invalid Cipher key asked:') 
                    print(str(valerr))
                    print('Returning (-1)') 

                    conn.sendall("-1".encode())
                else:
                    print('KM Cipher Received', cipher_mode)
                    return_key = CipherMode_switcher(cipher_mode)

                    #conn.sendall(data)
                    conn.sendall(return_key.encode())

