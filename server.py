import socket
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

    conn,addr= t_sock.accept()
    print(addr[0]+':'+str(addr[1])+' CONNECTED')
    data= conn.recv(1024)
    conn.close()
except Exception as err:
    print('CONNECTION_ACCEPT_ERROR : '+str(err))
    if conn is not None:
        conn.close()
    sys.exit()