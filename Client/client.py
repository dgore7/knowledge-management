import sys
import socket
import os
import time
import codecs


class Client:
    def __init__(self):
        print("Client Created")
        self.username = None
        

    def connect(self):
        host = 'localhost'
        port = 8001

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((host,port))
        print("Success")
        
        return sock


    def login(self, username, password):
        connection = self.connect()
        connection.send( "login".encode() )

        status_code = connection.recv(2)


        if status_code.decode() != "OK":
            print("Failled")
            return

        login_info = username + ":" + password

        print (login_info)

        connection.send(login_info.encode())
        #self.sock.send(login_info.encode())
        connection.close()
        self.username = username
        if username and password:
            return 1
        else:
            return 0

    def register(self, username, password):
        connection = self.connect()

        connection.send( "register".encode() )

        register_info = username + ":" + password
        connection.send(register_info.encode())

        connection.close()

        if username and password:
            return 1
        else:
            return 0

    def createGroup(self, group, members):
        connection = self.connect()

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
        connection = self.connect()

        connection.send("add".encode())
        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("Error")
            return

        connection.send(member_name.encode())

        connection.close()

        return "SUCCESS"

    def removeMember(self, member_name):
        connection = self.connect()

        connection.send("remove".encode())

        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("Error")
            return

        connection.send(member_name.encode())

        connection.close()

        return "SUCCESS"

    def upload(self, filename, tags, comments, repo):
        try:
            file_stat = os.stat(filename)
            file_exist = True
        except FileNotFoundError:
            file_exist = False

        if not file_exist:
            print("Error")
            return "FILE NOT FOUND"

        connection = self.connect()
        
        connection.send("upload".encode())

        status_code = connection.recv(2)

        if status_code.decode() != "OK":
            print("failed")
            return
        msg= filename + ":" + tags + ":" + comments

        connection.send( msg.encode() )
        status = connection.recv(64).decode()
        if status[:7] == "FAILURE":
            print(status[8:])

        print(filename)


        #print("Recent Access: " + str(time.gmtime(file_stat.st_atime)))
        #print("Year: " + str(time_date[0]))
        #print("Month: " + str(time_date[1]))
        #print("Day: " + str(time_date[2]))
        #print("Hour: " + str(time_date[3]))
        #print("Minute: " + str(time_date[4]))
        #print("Second: " + str(time_date[5]))
        #print("Week Day: " + str(time_date[6]))
        #print("Year Day: " + str(time_date[7]))

        print("Recent Modification: " + str(file_stat.st_mtime))
        time_date2 = time.gmtime(file_stat.st_mtime)
        print("Year: " + str(time_date2[0]))
        print("Month: " + str(time_date2[1]))
        print("Day: " + str(time_date2[2]))
        print("Hour: " + str(time_date2[3]))
        print("Minute: " + str(time_date2[4]))
        print("Second: " + str(time_date2[5]))
        print("Week Day: " + str(time_date2[6]))
        print("Year Day: " + str(time_date2[7]))

        print("Recent Metadata Change: " + str(file_stat.st_ctime))

        print("ID Owner: " + str(file_stat.st_uid))
        print("Group ID Owner: " + str(file_stat.st_gid))


        file = open(filename,"rb")
        #file = codecs.open(filename, "rb", "utf-8")

        print("Sending info")

        date_time = time.gmtime(file_stat.st_atime)
        file_date_info = str(date_time[0]) + \
                             "|" + str(date_time[1]) + \
                             "|" + str(date_time[2]) + \
                             "|" + str(date_time[3]) + \
                             "|" + repo

        connection.send(file_date_info.encode())

        status_code = connection.recv(7)

        if status_code.decode() != "SUCCESS":
            print("failed")
            return

        for line in file:
            print(line)
            #sys.stdout.write(line.decode())
            # sys.stdout.write(line.decode())
            connection.send(line)

        file.close()
        print("Closing file")
        connection.close()

        return "SUCCESS"

    def download(self, filename):
        connection = self.connect()
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
        connection = self.connect()
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
