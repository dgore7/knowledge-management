import sys
import socket


class Client:
    def __init__(self):
        host = 'localhost'
        port = 8001

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))
        print("Success")
        #message = "query:" + sys.stdin.readline()
        #self.sock.send(message.encode())

    def login(self, username, password):
        if username and password:
            return 1
        else:
            return 0

    def register(self, username, password):
        if username and password:
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        print(filename)
        print(category)
        print(keywords)

    def retrieve(self, filename):
        print(filename)

    def search(self, filename):
        print(filename)

    def delete(self, filename):
        print(filename)
