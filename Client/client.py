import os
import pickle
import socket
import ssl
import struct
import sys
from pickle import UnpicklingError
from socket import error as SocketError

from Client import SUCCESS, FAILURE, global_username
from Client import loginEncryption
from Client import repoids, SOCKET_EOF
from Client.client_c import client_api


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
            return 0
        connection = self.sock
        connection.send("register".encode())

        register = loginEncryption.LoginEncoding()
        register.setUsername(username)
        register.setPassword(password)
        username = register.getUsername()
        password = register.getPassword()
        password_salt = str(register.getPasswordSalt())

        register_info = "username:" + username + ";password:" + password + ";sec_question:" \
                        + sec_question + ";sec_answer:" + sec_answer + ";password_salt:" + password_salt
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
        """
        Takes the name of a group, and iterates through a list of usernames to add to the group.
        :param group: string
        :param members: list
        :return:
        """
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


    def addMember(self, member_name):
        """
        Takes a username and adds it to the group that it used within.

        :param member_name:
        :return:
        """
        connection = self.sock
        message = "member_add".encode()
        connection.send(message)
        status_code = connection.recv(2)

        if status_code != FAILURE:
            print("Error")
            return False

        message = member_name.encode()
        connection.send(message)
        result = connection.recv(2)
        if result == SUCCESS:
            return True
        else:
            return False

    def removeMember(self, member_name):
        connection = self.sock

        connection.send("member_remove".encode())

        status_code = connection.recv(2)

        if status_code != SUCCESS:
            print("Error")
            return False

        message = member_name.encode()
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
        print(tags)
        msg.extend(['mod_time:', mod_time, ';'])
        ######### Add statements to determine where to upload
        msg.extend(['gid:', repo, ';'])
        tags_buffer = ['tags:']
        tags_buffer.extend(tag + ',' for tag in tags)
        if tags: # remove last comma
            tags_buffer[-1] = tags_buffer[-1][:-1]
        msg.extend(tags_buffer)
        print(msg)
        msg = ''.join(msg)
        connection.send(msg.encode())
        status = connection.recv(2)
        if status != client_api.SUCCESS:
            print('ERROR')
            return False
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
            connection.send(line)
        connection.send(SOCKET_EOF)
        file.close()
        print("Closing file")
        return True
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
        connection = self.connect()
        connection.close()

    def retrieve(self, filename):
        connection = self.sock
        connection.send("retrieve".encode())

        connection.send(filename.encode())
        print(filename)
        # sock.close()

    def retrieve_repo(self, group_ids=None):
        connection = self.sock
        if not group_ids:
            raise RuntimeError('Arguements required')
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
            print("failed in retrieve groups2")
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
