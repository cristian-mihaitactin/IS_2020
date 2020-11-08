import socket, pickle
import sys
#import security_utils
#from security_utils import CipherMode
from security_utils import *

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_KM = 5001       # The port used by KM
PORT_A = 5002        # The port used by A
PORT_B = 5003        # The port used by B

def askKey(cipher_mode: CipherMode):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_km:
        s_km.connect((HOST, PORT_KM))

        s_km.sendall(bytes(str(int(cipher_mode)),'utf-8'))
        data = s_km.recv(1024)
        print('Received', repr(data))
        #print('Received',data.decode())
        decryptedKey = AES_dencrypt_singleblock(data)
        print('decryptedKey', decryptedKey)
        return decryptedKey

def process_response(cipherMode, data):
    if (cipherMode == CipherMode.CBC):
        return data.decode('utf-8')
    elif (cipherMode == CipherMode.OFB):
        return pickle.loads(data)
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_B))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(2048)
                if not data:
                    break

                print('B Received', data.decode('utf-8'))
                try:
                    cipherMode = CipherMode(int(data.decode('utf-8')))
                    print('B Cipher Received', cipherMode)
                    key = askKey(cipherMode)
                    print('B Key  Received', key)
                    #print('KM Received', int.from_bytes( data, byteorder='little'))
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    print('B Returning (-1)') 

                    conn.sendall("-1".encode())
                else:
                    conn.sendall("1".encode())

                    data = conn.recv(1024)
                    response = process_response(cipherMode, data)
                    
                    print('B second data', response)

                    decrypt_str = decryptMessage(cipherMode, key,response)
                    print('B decrypted:', decrypt_str)
