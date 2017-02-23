import sys
import socket
import os
import time

import codecs


class Client:
    def __init__(self):
        print("Client Created")

    def connect(self):
        host = 'localhost'
        port = 8001

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Success")

        return sock

    def login(self, username, password):
        connection = self.connect()
        connection.send("login".encode())
        print("Hello")
        status_code = connection.recv(2)
        print("MSG Replayed")

        if status_code.decode != "OK":
            print("Failled")
            return

        login_info = username + ":" + password

        print(login_info)

        connection.send(login_info.encode())
        # self.sock.send(login_info.encode())
        connection.close()
        if username and password:
            return 1
        else:
            return 0

    def register(self, username, password):
        sock = self.connect()
        sock.send("register".encode())

        register_info = username + ":" + password
        sock.send(register_info.encode())

        if username and password:
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        connection = self.connect()

        connection.send("upload".encode())

        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("failed")
            return
        msg = filename

        connection.send(msg.encode())
        status = connection.recv(64).decode()
        if status[:7] == "FAILURE":
            print(status[8:])
        try:
            file_stat = os.stat(filename)
            file_exist = True
        except FileNotFoundError:
            file_exist = False

        file = open(filename, "rb")
        # file = codecs.open(filename, "rb", "utf-8")
        for line in file:
            # sys.stdout.write(line.decode())
            connection.send(line)

        file.close()
        print("Closing file")
        connection.close()

    def retrieve(self, filename):
        sock = self.connect()
        sock.send("retrieve".encode())

        sock.send(filename.encode())
        print(filename)
        sock.close()

    def search(self, filename):
        sock = self.connect()
        sock.send("search".encode())

        # Maybe can use query statement here
        sock.send(filename.encode())
        print(filename)
        sock.close()

    def delete(self, filename):
        sock = self.connect()
        sock.send("delete".encode())
        sock.send(filename.encode())
        print(filename)
        sock.close()
