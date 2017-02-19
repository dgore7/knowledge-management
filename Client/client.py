import sys
import socket
import os
import time

import ssl
import hashlib


class Client:
    def __init__(self):
        self.connected = False

        # TODO: NEED TO ADD CODE TO IMPORT A PUB KEY (or cert) WHICH WE WILL PUT IN THE CLIENT FILES AHEAD OF TIME!


        host = 'localhost'
        port = 8001

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))
        print("Initialized")
        #message = "query:" + sys.stdin.readline()
        #self.sock.send(message.encode())

    def connect(self, host='localhost', port=8001, use_ssl=True):
        #parameter: host -> The desired host for the new connection.
        #parameter: port -> The desired port for the new connection.
        #parameter: use_ssl -> Can be set to False to disable SSL for the client connecting

        # Code to get the server's cert
        #cert = conn.getpeercert()
        #If it's self signed, I dont think we need a CA cert to verify?

        if not self.connected:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.secureSock = ssl.wrap_socket(self.sock, server_side = False)
            self.secureSock.connect((host, port))
            self.connected = True
            print("Secure connection successful!")
        else:
            print("Client already connected to a server! Disconnect first.")

    def disconnect(self):
        if self.connected:
            self.secureSock.shutdown()
            self.secureSock.close()
            self.connected = False
            print("Disconnection successful!")
        else:
            print("Nothing to disconnect!")

    def login(self, username, password):
        self.sock.send( "login".encode() )

        login_info = username + ":" + password
        self.sock.send(login_info.encode())
        if username and password:
            # Add password hashing code in here (use username as salt?)
            # Note that sha3_512 requires 3.6. sha512 is a less secure option
            # to maintain compatibility with older platforms
            hashedPass = hashlib.sha3_512(password.encode()).hexdigest()
            return 1
        else:
            return 0

    def register(self, username, password):
        self.sock.send( "register".encode() )

        register_info = username + ":" + password
        self.sock.send(register_info.encode())

        if username and password:
            # Add password hashing code in here (use username as salt?)
            # Note that sha3_512 requires 3.6. sha512 is a less secure option
            # to maintain compatibility with older platforms
            hashedPass = hashlib.sha3_512(password.encode()).hexdigest()
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        self.sock.send( "upload".encode() )

        msg= filename + ":" + category + ":" + keywords

        self.sock.send( msg.encode() )

        try:
            file_stat = os.stat(filename)
            file_exist = True
        except FileNotFoundError:
            file_exist = False

        file = open(filename)
        for line in file:
            print(line.rstrip('\n'))
            self.sock.send(line.encode())

        file.close()
        time.sleep(0.37)
        self.sock.send('0'.encode())
        print("Closing file")

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

    def close_socket(self):
        self.sock.close()
