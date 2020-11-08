import socket, pickle
import sys
#import security_utils
#from security_utils import CipherMode
from security_utils import *

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_KM = 5001       # The port used by KM
PORT_A = 5002        # The port used by A
PORT_B = 5003        # The port used by B

def prepareReply(cyphermode,encryptedMessage ):
    if (cyphermode == CipherMode.OFB):
        return pickle.dumps(encryptedMessage)
    return encryptedMessage

def sendToB(cyphermode:CipherMode, msg, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_b:
        s_b.connect((HOST, PORT_B))
        s_b.sendall(bytes(str(int(cyphermode)),'utf-8'))
        data = s_b.recv(1024)
        #print('Received', repr(data))
        response_str = str(data, 'utf-8')
        print('Received', response_str)
        
        if (response_str == "-1"):
            print("B responded with error:", response_str)
        elif (response_str == "1"):
            # Send messages to B with selected mode
            try:
                encryptedMessage = ecryptMessage(cyphermode,key,msg)
                reply = prepareReply(cyphermode,encryptedMessage )
                print('encryptedMessage=', reply)
                s_b.sendall(reply)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print("Unexpected error:", sys.exc_info()[1])
                print("Unexpected error:", sys.exc_info()[2])
                s_b.close()

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

def tema(cipher_mode:CipherMode, msg):
    # Call KM for CBC Key
    k1 = askKey(cipher_mode)
    # Call B and start exchanging messages
    sendToB(cipher_mode, msg, k1)

# Main work
msg = 'Tema 1. Sa speram ca se va decripta cum trebuie indiferent de lungimea mesajului.'
tema(CipherMode.CBC, msg)
tema(CipherMode.OFB, msg)

