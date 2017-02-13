import sys
import socket
import os


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
        self.sock.send( "login".encode() )

        login_info = username + ":" + password
        self.sock.send(login_info.encode())
        if username and password:
            return 1
        else:
            return 0

    def register(self, username, password):
        self.sock.send( "register".encode() )

        register_info = username + ":" + password
        self.sock.send(register_info.encode())

        if username and password:
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        self.sock.send( "upload".encode() )

        print(len(filename))
        msg= filename + ":" + category + ":" + keywords

        self.sock.send( (msg.encode() ) )

        try:
            file_stat = os.stat(filename)
            file_exist = True
        except FileNotFoundError:
            file_exist = False

        file = open(filename)

        for line in file.readlines():
            self.sock.send(line.encode())

        file.close()

    def retrieve(self, filename):
        self.sock.send("retrieve".encode())

        self.sock.send(filename.encode())

        print(filename)

    def search(self, filename):

        self.sock.send("search".encode())

        #Maybe can use query statement here
        self.sock.send(filename.encode())
        print(filename)

    def delete(self, filename):

        self.sock.send("delete".encode())
        self.sock.send(filename.encode())
        print(filename)
