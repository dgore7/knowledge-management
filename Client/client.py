import sys
import socket

import ssl
import hashlib


class Client:
    def __init__(self):
        self.connected = False

        # TODO: NEED TO ADD CODE TO IMPORT A PUB KEY (or cert) WHICH WE WILL PUT IN THE CLIENT FILES AHEAD OF TIME!


        #host = 'localhost'
        #port = 8001

        #self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.sock.connect((host,port))
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
        if username and password:
            # Add password hashing code in here (use username as salt?)
            # Note that sha3_512 requires 3.6. sha512 is a less secure option
            # to maintain compatibility with older platforms
            hashedPass = hashlib.sha3_512(password).hexdigest()
            return 1
        else:
            return 0

    def register(self, username, password):
        if username and password:
            # Add password hashing code in here (use username as salt?)
            # Note that sha3_512 requires 3.6. sha512 is a less secure option
            # to maintain compatibility with older platforms
            hashedPass = hashlib.sha3_512(password).hexdigest()
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
