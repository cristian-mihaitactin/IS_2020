import socket
import security_utils
from security_utils import CipherMode

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_KM = 5001       # The port used by KM
PORT_A = 5002        # The port used by A
PORT_B = 5003        # The port used by B

#print ('k3_', security_utils.K3)

def sendToB():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_b:
        #s_km.connect((HOST, PORT_KM))
        s_b.connect((HOST, PORT_B))
        #s.sendall(b'Hello, world')
        #print(int(CipherMode.CBC))
        s_b.sendall(bytes(str(int(CipherMode.CBC)),'utf-8'))
        
        data = s_b.recv(1024)

    print('Received', repr(data))

def askKey(cipher_mode: CipherMode):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_km:
        s_km.connect((HOST, PORT_KM))

        s_km.sendall(bytes(str(int(cipher_mode)),'utf-8'))
        
        data = s_km.recv(1024)
        #print('Received', repr(data))
        print('Received',data.decode())

askKey(CipherMode.CBC)
askKey(CipherMode.OFB)



