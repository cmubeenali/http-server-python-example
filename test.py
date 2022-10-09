from http.server import HTTPServer, BaseHTTPRequestHandler

server= HTTPServer(server_address=('0.0.0.0',8000),RequestHandlerClass=BaseHTTPRequestHandler,bind_and_activate=True)
conn,addr= server.socket.accept()

request=BaseHTTPRequestHandler(conn,client_address=(addr[0],addr[1]),server=server)

print(request.headers)