import sys
import socket

if __name__ == '__main__':
    print("enter a query:")
    port = 8001 if len(sys.argv) != 2 else sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", int(port)))
    message = "query:" + sys.stdin.readline()
    sock.send(message.encode())
    # sock.close()