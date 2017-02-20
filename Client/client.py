import sys
import socket
import os
import time

import codecs
import ssl
import hashlib


class Client:
    def __init__(self):
        self.connected = False

        # TODO: NEED TO ADD CODE TO IMPORT A PUB KEY (or cert) WHICH WE WILL PUT IN THE CLIENT FILES AHEAD OF TIME!


        host = 'localhost'
        port = 8001

        #self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.sock.connect((host,port))
        self.connect()
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
        connection = self.connect()
        connection.send( "login".encode() )
        print("Hello")
        status_code = connection.recv(2)
        print("MSG Replayed")

        if status_code.decode != "OK":
            print("Failled")
            return

        login_info = username + ":" + password

        print (login_info)

        connection.send(login_info.encode())
        #self.sock.send(login_info.encode())
        connection.close()
        if username and password:
            # Add password hashing code in here (use username as salt?)
            # Note that sha3_512 requires 3.6. sha512 is a less secure option
            # to maintain compatibility with older platforms
            #hashedPass = hashlib.sha3_512(password.encode()).hexdigest()
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
            #hashedPass = hashlib.sha3_512(password.encode()).hexdigest()
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        connection = self.connect()
        
        connection.send( "upload".encode() )

        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("failed")
            return
        msg= filename

        connection.send( msg.encode() )
        status = connection.recv(64).decode()
        if status[:7] == "FAILURE":
            print(status[8:])
        try:
            file_stat = os.stat(filename)
            file_exist = True
        except FileNotFoundError:
            file_exist = False

        file = open(filename, "rb")
        #file = codecs.open(filename, "rb", "utf-8")
        for line in file:
            connection.send(line)

        file.close()
        print("Closing file")
        connection.close()

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
        connection = self.connect()
        connection.close()

