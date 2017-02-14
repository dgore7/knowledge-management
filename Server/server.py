import sys
import socket
from request_handler import RequestHandler
from server_globals import connections


def create_socket(port, host='localhost'):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    print("Server started on {}:{}".format(host, port))
    return server


def server_loop(server):
    while True:
        sock, addr = server.accept()
        print("Recieved new connection from {}.".format(addr))
        connections.append(sock)
        handler = RequestHandler(sock)
        handler.start()


if __name__ == '__main__':
    server = create_socket(sys.argv[1] if len(sys.argv) >= 2 else 8001)
    server.listen(10)
    server_loop(server)