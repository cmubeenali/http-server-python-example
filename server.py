import base64
import socket
import struct
import sys

HOST='0.0.0.0'
PORT=8000

t_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

try:
    t_sock.bind((HOST,PORT))
except socket.error as err:
    print("bind failed : "+str(err))
    sys.exit()

conn=None
addr=None
try:
    t_sock.listen(1)    

    print('LISTENING ON '+HOST+':'+str(PORT))

    i=0
    while i<5:
        conn,addr= t_sock.accept()
        conn.setblocking(0)
        
        print(addr[0]+':'+str(addr[1])+' CONNECTED')
        data=bytearray()
        while True:            
            try:
                packet= conn.recv(1024)                
                data.extend(packet)
                if len(packet)<1024:
                    break
            except Exception as err:
                break
        print('DATA RECEIVED : '+data.decode('utf-8'))
        resp="""HTTP/1.1 404 Not Found
        Content-Type: text/html

        Not Found
        """.encode()
        conn.send(resp)
        conn.close()
        i+=1
    t_sock.close()
except Exception as err:
    print('CONNECTION_ACCEPT_ERROR : '+str(err))
    if conn is not None:
        conn.close()
    t_sock.close()
    sys.exit()