import socket
import security_utils
from security_utils import CipherMode

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_KM = 5001       # The port used by KM
PORT_A = 5002        # The port used by A
PORT_B = 5003        # The port used by B

print ('k3_', security_utils.K3)
'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT_KM))
    #s.sendall(b'Hello, world')
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))
'''

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_B))
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
                print('KM Cipher Received', CipherMode(int(data.decode('utf-8'))))
                #print('KM Received', int.from_bytes( data, byteorder='little'))
                
                conn.sendall(data)

