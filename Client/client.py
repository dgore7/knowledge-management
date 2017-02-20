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

        #self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.sock.connect((host,port))
        self.connect()
        print("Initialized")
        #message = "query:" + sys.stdin.readline()
        #self.sock.send(message.encode())

    def connect(self, host='localhost', port=8001):
        #parameter: host -> The desired host for the new connection.
        #parameter: port -> The desired port for the new connection.
        #parameter: use_ssl -> Can be set to False to disable SSL for the client connecting

        # Code to get the server's cert
        # We need this to verify it (the cert is its own root)
        #cert = conn.getpeercert()

        if not self.connected:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Defaults to SSL/TLS support
            context.verify_mode = ssl.CERT_REQUIRED # ssl.CERT_REQUIRED is more secure
            context.check_hostname = True  # Hostname verification on certs (Dont want for now)
            context.load_verify_locations(cafile='/Users/jsmith/Documents/CSC376/keyfiles/KnowledgeManagement.crt')
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock = context.wrap_socket(self.sock, server_side = False,server_hostname='lpc-depaulsecure-219-223.depaulsecure-student.depaul.edu')

            self.sock.connect((host, port))
            self.connected = True
            print("Secure connection successful!")
        else:
            print("Client already connected to a server! Disconnect first.")

    def disconnect(self):
        if self.connected:
            self.sock.shutdown()
            self.sock.close()
            self.connected = False
            print("Disconnection successful!")
        else:
            print("Nothing to disconnect!")

    def login(self, username, password):
        self.sock.send("login".encode())

        login_info = username + ":" + password
        self.sock.send(login_info.encode())
        if self.sock.recv(1024).decode() == "login_status|ok":
            return 1
        else:
            return 0

        #if username and password:
        #
        #   return 1
        #else:
        #    return 0

    def register(self, username, password):
        self.sock.send("register".encode())

        register_info = username + ":" + password
        self.sock.send(register_info.encode())

        if username and password:
            # Add password hashing code in here (use username as salt?)
            # Note that sha3_512 requires 3.6. sha512 is a less secure option
            # to maintain compatibility with older platforms
            #hashedPass = hashlib.sha3_512(password.encode()).hexdigest()
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        self.sock.send("upload".encode())

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
