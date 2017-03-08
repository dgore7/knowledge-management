import sys
import socket
import os
import time

import pickle

import codecs
import ssl
from Client import auth_client
from Client.client_c import client_api
from Client import loginEncryption

# import OpenSSL


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

    def connect(self, cert_file_path=os.path.normpath(os.path.join(os.getcwd(), '../KnowledgeManagement.crt')),
                host='localhost', port=8001):
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
        if decoded_status_code != client_api.SUCCESS:
            print("Failled")
            return

        # username = loginEncryption.LoginEncoding.loginEncryption(username)
        # password = loginEncryption.LoginEncoding.passwordHashing(username, password)
        login_info = "username:" + username + ";" + "password:" + password


        print(login_info)

        connection.send(login_info.encode())
        # self.sock.send(login_info.encode())
        # connection.close()
        server_response = connection.recv(2).decode()  # "login_response|bad" or "login_response|good"
        if server_response == client_api.SUCCESS:
            return 1
        else:
            return 0

    def register(self, username, password):
        if self.connected == False:
            return 0  # Maybe change to a unique code stating we are not connected?
        connection = self.sock
        connection.send("register".encode())

        register_info = "username:" + username + ";" + "password:" + password
        connection.send(register_info.encode())
        server_response = connection.recv().decode()
        if server_response == client_api.SUCCESS:
            return 1
        else:
            return 0

    def upload(self, filename, tags, notes):
        connection = self.sock

        connection.send("upload".encode())

        status_code = connection.recv(1024).decode()

        if status_code != client_api.SUCCESS:
            print("failed")
            return
        msg = ['filename:', filename, ';']
        msg.extend(['notes:', notes, ';'])
        msg.extend(['tags:'].extend(tag + ',' for tag in tags))
        msg = ''.join(msg)
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
        # connection.close()

    def retrieve(self, filename):
        connection = self.sock
        connection.send("retrieve".encode())

        connection.send(filename.encode())
        print(filename)
        # sock.close()

    def retrieve_repo(self, group_id=None, username=None):
        connection = self.sock
        if not group_id and not username:
            raise RuntimeError('Arguements required')
        connection.send("retrieve repo".encode())
        result = connection.recv(1024).decode()
        if not result == SUCCESS:
            print(result)
            return []
        if group_id:
            connection.send(str(group_id).encode())
        elif username:
            connection.send(username.encode())
        result = []
        while True:
            bytes_received = connection.recv(1024)
            if bytes_received:
                result.append(bytes_received)
            else:
                break
        result = b''.join(result)
        return pickle.loads(result)

    def search(self, filename):
        connection = self.sock
        connection.send("search".encode())

        # Maybe can use query statement here
        connection.send(filename.encode())
        print(filename)
        # sock.close()

    def delete(self, filename, group_id):
        connection = self.sock
        connection.send("delete".encode())
        if not connection.recv(2).decode() == client_api.SUCCESS:
            return False
        msg = 'filename:' + filename + ';group_id:' + group_id
        connection.send(msg.encode())
        result = connection.recv(1024).decode()
        if result != client_api.SUCCESS:
            print(result)
            return False
        return True
        # sock.close()

    if __name__ == '__main__':
        print("enter a query:")
        port = 8001 if len(sys.argv) != 2 else sys.argv[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", int(port)))
        message = "query:" + sys.stdin.readline()
        sock.send(message.encode())
        # sock.close()