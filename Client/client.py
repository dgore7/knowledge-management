import sys
import socket
import os
import time

import ssl
import hashlib
from . import client_c
import codecs


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
        print("Client Created")
        

    def connect_insecure(self):
        host = 'localhost'
        port = 8001

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((host,port))
        print("Success")
        
        return sock

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
            context.load_default_certs() # Load the default certificates in case the server is not using a self-signed key
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
        self.sock.send(client_c.client_api.login_code.encode())

        login_info = username + "|" + password
        self.sock.send(login_info.encode())
        if self.sock.recv(1024).decode() == client_c.client_api.login_status_code + client_c.client_api.data_separator + client_c.client_api.login_status_good:
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
            return 1
        else:
            return 0

    def register(self, username, password):
        self.sock.send(client_c.client_api.register_code)

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
        self.sock.send(client_c.client_api.upload_code)
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
        self.sock.send(client_c.client_api.retrieve_code)

        self.sock.send(filename.encode())


        print(filename)

    def search(self, filename):

        self.sock.send(client_c.client_api.search_code)

        #Maybe can use query statement here
        self.sock.send(filename.encode())
        print(filename)

    def delete(self, filename):

        self.sock.send(client_c.client_api.delete_code)
        self.sock.send(filename.encode())
        print(filename)

    def close_socket(self):
        connection = self.connect()
        connection.close()

