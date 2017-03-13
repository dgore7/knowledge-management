import sys
import socket
import os
import time

import pickle

from Client import client_c
from Client.client_c import client_api
import codecs
import ssl
from Client.client_c import client_api
from Client.loginEncryption import LoginEncoding
from Client import g_personal_repoid, SOCKET_EOF
from socket import error as SocketError


class Client:
    """Main file on client side"""

    def __init__(self):
        'Intilizes the client'
        self.connected = False
        self.connect()
        print("Initialized")

    def connect(self, cert_file_path=os.path.normpath(os.path.join(os.getcwd(), '../KnowledgeManagement.crt')),
                host='localhost', port=8001):
        """Creates a secure socket layer (SSL) connection after verifying the certificate"""

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
        """Closes the client's connection to the socket"""

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

        login_info = "username:" + username + ";" + "password:" + password
        print(login_info)

        connection.send(login_info.encode())
        server_response = connection.recv(2)  # "login_response|bad" or "login_response|good"
        print(server_response.decode())
        if server_response == client_api.SUCCESS:
            g_personal_repoid = connection.recv(32).decode()
            return 1
        else:
            return 0

    def register(self, username, password, sec_question, sec_answer):
        """Takes the parameters, hashes the password, encodes the username, and prepares it to be sent to server"""

        if self.connected == False:
            return False
        connection = self.sock
        connection.send("register".encode())

        register_info = "username:" + username + "; password:" + password + "; sec_question" \
                        + sec_question + "; sec_answer" + sec_answer
        connection.send(register_info.encode())
        server_response = connection.recv(2)
        if server_response == client_api.SUCCESS:
            return True
        else:
            return False

    def createGroup(self, group, members):
        """
        Takes the name of a group, and iterates through a list of usernames to add to the group.
        :param group: string
        :param members: list
        :return:
        """
        connection = self.sock

        connection.send("create_group".encode())

        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("Error")
            return

        connection.send(group.encode())

        status_code = connection.recv(7)

        if status_code.decode() != "SUCCESS":
            print("Error")
            return

        for member in members:
            connection.send(member.encode())
            connection.recv(5)

        connection.send("DONE".encode())

        print(group)
        print(members)
        connection.close()

        return "SUCCESS"

    def addMember(self, member_name):
        """
        Takes a username and adds it to the group that it used within.

        :param member_name:
        :return:
        """
        connection = self.sock

        connection.send("addMemGrp".encode())
        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("Error")
            return

        connection.send(member_name.encode())

        connection.close()

        return "SUCCESS"

    def removeMember(self, member_name):
        connection = self.sock

        connection.send("removeMemGrp".encode())

        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("Error")
            return

        connection.send(member_name.encode())

        connection.close()

        return "SUCCESS"

    def upload(self, filename, tags, notes, repo):
        connection = self.sock

        connection.send("upload".encode())

        status_code = connection.recv(2)

        if status_code != client_api.SUCCESS:
            print("failed")
            return
        msg = ['fname:', filename.split('/')[-1], ';']
        msg.extend(['notes:', notes, ';'])
        print(tags)
        msg.extend(['gid:', repo, ';'])
        tags_buffer = ['tags:']
        tags_buffer.extend(tag + ',' for tag in tags)
        if tags:
            tags_buffer[-1] = tags_buffer[-1][:-1]
        msg.extend(tags_buffer)
        msg = ''.join(msg)
        connection.send(msg.encode())
        status = connection.recv(2)
        if status != client_api.SUCCESS:
            print('ERROR')
            return
        # try:
        #     file_stat = os.stat(filename)
        #     file_exist = True
        # except FileNotFoundError:
        #     file_exist = False
        #
        # #print("Recent Access: " + str(time.gmtime(file_stat.st_atime)))
        # #print("Year: " + str(time_date[0]))
        # #print("Month: " + str(time_date[1]))
        # #print("Day: " + str(time_date[2]))
        # #print("Hour: " + str(time_date[3]))
        # #print("Minute: " + str(time_date[4]))
        # #print("Second: " + str(time_date[5]))
        # #print("Week Day: " + str(time_date[6]))
        # #print("Year Day: " + str(time_date[7]))
        #
        # print("Recent Modification: " + str(file_stat.st_mtime))
        # time_date2 = time.gmtime(file_stat.st_mtime)
        # print("Year: " + str(time_date2[0]))
        # print("Month: " + str(time_date2[1]))
        # print("Day: " + str(time_date2[2]))
        # print("Hour: " + str(time_date2[3]))
        # print("Minute: " + str(time_date2[4]))
        # print("Second: " + str(time_date2[5]))
        # print("Week Day: " + str(time_date2[6]))
        # print("Year Day: " + str(time_date2[7]))
        #
        # print("Recent Metadata Change: " + str(file_stat.st_ctime))
        #
        # print("ID Owner: " + str(file_stat.st_uid))
        # print("Group ID Owner: " + str(file_stat.st_gid))


        # #file = codecs.open(filename, "rb", "utf-8")
        #
        # print("Sending info")
        #
        # date_time = time.gmtime(file_stat.st_atime)
        # file_date_info = str(date_time[0]) + \
        #                      "|" + str(date_time[1]) + \
        #                      "|" + str(date_time[2]) + \
        #                      "|" + str(date_time[3]) + \
        #                      "|" + repo
        #
        # connection.send(file_date_info.encode())
        #
        # status_code = connection.recv(7)

        file = open(filename, "rb")

        for line in file:
            print(line)
            connection.send(line)
        connection.send(SOCKET_EOF)
        file.close()
        print("Closing file")
        # connection.close()

    def download(self, filename):
        connection = self.sock
        connection.send("download".encode())

        status_code = connection.recv(2)

        connection.send(filename.encode())

        print("Sent: " + filename)

        file = open(filename, 'wb')

        while True:
            line = connection.recv(1024)
            if not len(line):
                break
            else:
                file.write(line)

        file.close()

    # def search(self, filename):
    #     connection = self.connect()
    #
    #     connection.send("search".encode())
    #
    #     status_code = connection.recv(2)
    #
    #     #Maybe can use query statement here
    #     connection.send(filename.encode())
    #     print(filename)
    #
    #     connection.close()

    def filter_search(self, tags, keywords):
        print(tags)
        print(keywords)

    def delete(self, filename):
        connection = self.sock
        connection.send("delete".encode())

        status_code = connection.recv(2)

        connection.send(filename.encode())
        print(filename)

        status = None

        repay = connection.recv(7)
        if repay.decode() != "SUCCESS":
            status = 1

        else:
            status = 0

        connection.close()

        print(status)

        return status

    def close_socket(self):
        connection = self.sock
        connection.close()

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
        if not result == client_api.SUCCESS:
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
