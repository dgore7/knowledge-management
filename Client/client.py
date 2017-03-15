__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"



import sys
import socket
import os
import struct

import pickle

from pickle import UnpicklingError

from Client import client_c, SUCCESS, FAILURE, global_username
from Client import loginEncryption
from Client.client_c import client_api
import codecs
import ssl
# from Client import auth_client
from Client.client_c import client_api
from Client import repoids, SOCKET_EOF
from socket import error as SocketError


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
            try:
                self.sock.shutdown(socket.SHUT_WR)
                self.sock.close()
                self.connected = False
            except SocketError as e:
                print("Server must have disconnected first!")

            print("Disconnection successful!")
        else:
            print("Nothing to disconnect!")

    def login(self, username, password):
        """Takes the login information, ecrypts it, and prepares it to be sent to the server."""

        connection = self.sock

        connection.send("login".encode())
        status_code = connection.recv(2)

        if status_code != client_api.SUCCESS:
            print("Failled")
            return 0

        register = loginEncryption.LoginEncoding()
        register.setUsername(username)
        register.setPassword(password)
        username = register.getUsername()
        password = register.getPassword()

        login_info = "username:" + username + ";password:" + password

        connection.send(login_info.encode())

        server_response = connection.recv(2)  # SUCCESS or FAILURE
        print(server_response.decode())
        if server_response == client_api.SUCCESS:
            repoids.clear()
            packed_repo_id = connection.recv(4)
            repo_id_tup = struct.unpack('<L', packed_repo_id)
            repo_id = repo_id_tup[0]
            repoids.append(repo_id)
            print(repo_id)
        else:
            return 0

        global_username.clear()
        global_username.append(username)
        return 1

    def register(self, username, password, sec_question, sec_answer):
        """Takes the parameters, hashes the password, encodes the username, and prepares it to be sent to server"""

        if self.connected == False:
            print("how'd I get here??")
            return 0
        connection = self.sock
        connection.send("register".encode())

        register_info = "username:" + username + ";" + "password:" + password
        register = loginEncryption.LoginEncoding()
        register.setUsername(username)
        register.setPassword(password)
        username = register.getUsername()
        password = register.getPassword()

        register_info = "username:" + username + ";password:" + password + ";sec_question:" \
                        + sec_question + ";sec_answer:" + sec_answer
        connection.send(register_info.encode())
        server_response = connection.recv(2)
        if server_response == client_api.SUCCESS:
            repoids.clear()
            packed_repo_id = connection.recv(4)
            repo_id_tup = struct.unpack('<L', packed_repo_id)
            repo_id = repo_id_tup[0]
            repoids.append(repo_id)
            print(repo_id)
        else:
            return 0

        global_username.clear()
        global_username.append(username)
        return 1

    def createGroup(self, group, members):
        connection = self.sock

        connection.send("create_group".encode())

        status_code = connection.recv(2)

        if status_code != SUCCESS:
            print("Error")
            return -1
        message = []
        message.append("gname:")
        message.append(group)
        message.append(";")
        message.append("members:")
        for i in members:
            message.append(i)
            message.append(",")
        if members:
            message.pop()
        message = ''.join(message)
        message = message.encode()
        connection.send(message)
        result = connection.recv(2)
        if result != SUCCESS:
            return -1

        packed_gid = connection.recv(4)
        gid = struct.unpack("<L", packed_gid)
        repoids.append(gid)
        return 1


    def addMember(self, gid, member_name):
        connection = self.sock
        message = "member_add".encode()
        connection.send(message)
        status_code = connection.recv(2)

        if status_code != SUCCESS:
            print("Error")
            return False

        message = "gid:{};uname:{}".format(gid, member_name)
        message = message.encode()
        connection.send(message)
        result = connection.recv(2)
        if result == SUCCESS:
            return True
        else:
            return False

    def removeMember(self, gid, member_name):
        connection = self.sock

        connection.send("member_remove".encode())
        status_code = connection.recv(2)

        if status_code != SUCCESS:
            print("Error")
            return False

        message = "gid:{};uname:{}".format(gid, member_name)
        message = message.encode()
        connection.send(message)
        result = connection.recv(2)
        if result == SUCCESS:
            return True
        else:
            return False

    def upload(self, filename, tags, notes, repo):
        try:
            file_stat = os.stat(filename)
            file_exist = True
        except FileNotFoundError:
            file_exist = False
            return 0
        mod_time = str(file_stat.st_mtime)

        connection = self.sock

        connection.send("upload".encode())

        status_code = connection.recv(2)

        if status_code != client_api.SUCCESS:
            print("failed")
            return False
        msg = ['fname:', filename.split('/')[-1], ';']
        msg.extend(['notes:', notes, ';'])
        msg.extend(['size:', str(file_stat.st_size), ';'])
        msg.extend(['mod_time:', mod_time, ';'])
        msg.extend(['gid:', repo, ';'])
        print(tags)
        tags_buffer = ['tags:']
        tags_buffer.extend(tag + ',' for tag in tags)
        if tags:  # remove last comma
            tags_buffer[-1] = tags_buffer[-1][:-1]
        msg.extend(tags_buffer)
        print(msg)
        msg = ''.join(msg)
        connection.send(msg.encode())
        status = connection.recv(2)
        if status != client_api.SUCCESS:
            print('ERROR')
            return False

        file = open(filename, "rb")

        for line in file:
            connection.send(line)
        connection.send(SOCKET_EOF)
        file.close()
        print("Closing file")
        return True

    def download(self, filename, gid):
        if not filename or not gid:
            return False
        connection = self.sock
        connection.send("download".encode())

        status_code = connection.recv(2)
        if status_code != SUCCESS:
            print("An error occurred when trying to download a file.")
            return False

        message = ['filename:', filename, ';']
        message.extend(['gid:', gid])
        message = ''.join(message)
        message = message.encode()
        connection.send(message)

        status_code = connection.recv(2)
        if status_code != SUCCESS:
            print("An error occurred when trying to download a file.")
            return False

        print("Sent: " + filename)
        file = open(filename, 'wb')

        while True:
            line = connection.recv(1024)
            if line == SOCKET_EOF:
                break
            else:
                file.write(line)

        file.close()

    def retrieve_repo(self, group_ids=None):
        connection = self.sock
        if not group_ids:
            return []
        connection.send("retrieve_repo".encode())
        result = connection.recv(2)
        if not result == client_api.SUCCESS:
            print(result)
            return []
        msg = 'group_ids:' + ','.join(str(gid) for gid in group_ids)
        msg = msg.encode()
        connection.send(msg)

        result = connection.recv(2)
        if not result == client_api.SUCCESS:
            print(result)
            return []

        # python string builder pattern
        result = []
        while True:
            bytes_received = connection.recv(1024)
            if bytes_received == SOCKET_EOF:
                break
            elif bytes_received:
                result.append(bytes_received)

        print(result)
        result = b''.join(result)
        return pickle.loads(result)

    def retrieve_groups(self, username):
        connection = self.sock
        connection.send("groups_retrieve".encode())
        result = connection.recv(1024)

        if result != SUCCESS:
            print("failed in retrieve groups1")
            return []

        message = "username:" + username
        message = message.encode()
        connection.send(message)
        result = connection.recv(2)

        if result != SUCCESS:
            print("No groups found")
            return []

        chunks = []
        while True:
            bytes_received = connection.recv(1024)
            if bytes_received == SOCKET_EOF:
                break
            else:
                chunks.append(bytes_received)
        result = b''.join(chunks)
        try:
            groups = pickle.loads(result)
        except UnpicklingError:
            return []
        return groups

    def get_group_members(self, gid):
        if not gid:
            return []
        connection = self.sock
        connection.send("groups_get_member".encode())
        result = connection.recv(2)

        if result != SUCCESS:
            print("failed in retrieve members")
            return []

        message = "gid:" + str(gid)
        message = message.encode()
        connection.send(message)
        result = connection.recv(2)

        if result != SUCCESS:
            print("No members found")
            return []

        members = []
        while True:
            bytes_received = connection.recv(64)
            if bytes_received == SOCKET_EOF:
                break
            else:
                members.append(bytes_received.decode())
        return members

    def delete(self, filename, group_id):
        connection = self.sock
        connection.send("delete".encode())
        if not connection.recv(2) == SUCCESS:
            return False
        msg = 'filename:' + filename + ';group_id:' + group_id
        msg = msg.encode()
        connection.send(msg)
        result = connection.recv(2)
        if result != SUCCESS:
            print(result)
            return False
        return True

    def close_socket(self):
        connection = self.connect()
        connection.close()

if __name__ == '__main__':
    print("enter a query:")
    port = 8001 if len(sys.argv) != 2 else sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", int(port)))
    message = "query:" + sys.stdin.readline()
    sock.send(message.encode())
