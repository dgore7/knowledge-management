import sys
import socket
import os
import time

import codecs
import ssl
#import OpenSSL


class Client:
    def __init__(self):
        self.connected = False

        # TODO: NEED TO ADD CODE TO IMPORT A PUB KEY (or cert) WHICH WE WILL PUT IN THE CLIENT FILES AHEAD OF TIME!

        # self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.sock.connect((host,port))
        # TODO: ALTER ROUTINES TO INSTEAD CONNECT USING A CONNECT BUTTON. THEN CERTS CAN BE SET BEFOREHAND!
        self.connect()
        print("Initialized")
        # message = "query:" + sys.stdin.readline()
        # self.sock.send(message.encode())

    def connect(self, cert_file_path = '/Users/jsmith/Documents/CSC376/keyfiles/KnowledgeManagement.crt', host='localhost', port=8001):
        # parameter: host -> The desired host for the new connection.
        # parameter: port -> The desired port for the new connection.
        # parameter: use_ssl -> Can be set to False to disable SSL for the client connecting

        # Code to get the server's cert
        # We need this to verify it (the cert is its own root)
        # cert = conn.getpeercert()

        if not self.connected:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Defaults to SSL/TLS support
            context.verify_mode = ssl.CERT_REQUIRED  # ssl.CERT_REQUIRED is more secure
            context.check_hostname = True  # Hostname verification on certs (Dont want for now)
            # TODO: Alter the SSL location
            context.load_verify_locations(cafile=cert_file_path)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = context.wrap_socket(self.sock, server_side=False,
                                            server_hostname=socket.gethostname())

            # TODO: Add a try for the line below to handle certificate mismatch errors and others
            self.sock.connect((host, port))
            self.connected = True
            print("Secure connection successful!")
        else:
            print("Client already connected to a server! Disconnect first.")

    def disconnect(self):
        if self.connected:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.connected = False
            print("Disconnection successful!")
        else:
            print("Nothing to disconnect!")

    def login(self, username, password):
        connection = self.sock
        connection.send("login".encode())
        print("Hello")
        status_code = connection.recv(2)
        print("MSG Replayed")
        decoded_status_code = status_code.decode()

        if decoded_status_code != "OK":
            print("Failled")
            return

        login_info = username + ":" + password

        print(login_info)

        connection.send(login_info.encode())
        #self.sock.send(login_info.encode())
        #connection.close()
        server_response = connection.recv(19).decode().split("|") #"login_response|bad" or "login_response|good"
        if server_response[0] == "login_response" and server_response[1] == "good":
            return 1
        else:
            return 0

    def register(self, username, password):
        if self.connected == False:
            return 0  # Maybe change to a unique code stating we are not connected?
        connection = self.sock
        connection.send("register".encode())

        register_info = username + ":" + password
        connection.send(register_info.encode())

        if username and password:
            return 1
        else:
            return 0

    def upload(self, filename, category, keywords):
        connection = self.sock
        
        connection.send("upload".encode())

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
            #sys.stdout.write(line.decode())
            connection.send(line)

        file.close()
        print("Closing file")
        #connection.close()

    def retrieve(self, filename):
        connection = self.sock
        connection.send("retrieve".encode())

        connection.send(filename.encode())
        print(filename)
        #sock.close()

    def search(self, filename):
        connection = self.sock
        connection.send("search".encode())

        #Maybe can use query statement here
        connection.send(filename.encode())
        print(filename)
        #sock.close()

    def delete(self, filename):
        connection = self.sock
        connection.send("delete".encode())
        connection.send(filename.encode())
        print(filename)
        #sock.close()