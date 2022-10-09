
import socket
import sys
from urllib.request import BaseHandler
from process_request import make_app

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
        # conn.setblocking(0)
        
        # print(addr[0]+':'+str(addr[1])+' CONNECTED')
        # data=bytearray()
        # while True:            
        #     try:
        #         packet= conn.recv(1024)                
        #         data.extend(packet)
        #         if len(packet)<1024:
        #             break
        #     except Exception as err:
        #         break
        # print('DATA RECEIVED : '+data.decode('utf-8'))        
        
        application=make_app()
        # from werkzeug.serving import WSGIRequestHandler, BaseWSGIServer
        from socketserver import BaseRequestHandler
        from wsgiref.handlers import SimpleHandler,read_environ
        from werkzeug.serving import WSGIRequestHandler
        from http.server import BaseHTTPRequestHandler,HTTPServer
        http_server=HTTPServer(server_address=(HOST,PORT),RequestHandlerClass=BaseHTTPRequestHandler,bind_and_activate=False)
        # http_server.ssl_context=None
        # http_server.multithread=False
        # http_server.multiprocess=False
        
        # base_request= WSGIRequestHandler(request=conn,client_address=(HOST,PORT),server=http_server)
        # wsgi_base= SimpleHandler(stdin=None,stdout=None,stderr=None,environ=read_environ())
        # wsgi_base.setup_environ()
        # env= WSGIRequestHandler.make_environ(BaseHTTPRequestHandler(request=conn,client_address=(addr[0],addr[1]),server=None))
        # application(env=wsgi_base.environ,start_resp=wsgi_base.start_response)
        request= BaseHTTPRequestHandler(conn,client_address=(addr[0],addr[1]),server=http_server)

        resp="""HTTP/1.1 101 Switching Protocols
        Upgrade: websocket
        Connection: Upgrade
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