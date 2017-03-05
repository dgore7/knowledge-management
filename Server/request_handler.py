import threading
from tkinter import filedialog
from tkinter import *

from Server import connections

from Server.controllers import file_controller as f_ctrlr, user_controller as u_ctrlr


class RequestHandler(threading.Thread):
    """ A request handler class which runs in it's own thread """
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        connections.append(self.connection)
        print("Connection made")
        self.username = ""


    def run(self):
        raw_request = self.connection.recv(2048)
        print(raw_request)

        if len(raw_request):
            client_option = raw_request.decode()
            print("CO: " + client_option)

            if client_option == "login":
                self.connection.send("OK".encode())
                msg = self.connection.recv(1024)
                user_info = msg.decode()
                print("Logging in with: " + user_info)
                self.username = user_info.split(":")[0]
                print(self.username)
                u_ctrlr.login_user(msg)


            elif client_option == "register":
                msg = self.connection.recv(1024)
                print("Registering user: " + msg.decode())
                u_ctrlr.register_user(msg)

            elif client_option == "create_group":
                self.connection.send("OK".encode())
                group_name = self.connection.recv(1024)
                print("Creating Group: " + group_name.decode())
                self.connection.send("SUCCESS".encode())
                members = []
                while True:
                    member = self.connection.recv(1024)
                    if member.decode() == "DONE":
                        break
                    print("Member: " + member.decode())
                    members.append(member.decode())
                    self.connection.send("ADDED".encode())

                u_ctrlr.create_group(group_name, members)

            elif client_option == "add":
                self.connection.send("OK".encode())
                member_name = self.connection.recv(1024)
                print("Adding: " + member_name.decode())
                u_ctrlr.add_member(member_name)

            elif client_option == "remove":
                self.connection.send("OK".encode())
                member_name = self.connection.recv(1024)
                print("Removing: " + member_name.decode())
                u_ctrlr.remove_member(member_name)


            elif client_option == "upload":
                self.connection.send("OK".encode())
                msg = self.connection.recv(1024)
                print ("Received: " + msg.decode())
                f_ctrlr.upload_file(self.connection, msg)


            elif client_option == "download":
                self.connection.send("OK".encode())
                msg = self.connection.recv(1024)
                print("Retrieving File: " + msg.decode())
                f_ctrlr.download_file(self.connection, msg)


            elif client_option == "delete":
                self.connection.send("OK".encode())
                msg = self.connection.recv(1024)
                print("Deleting file: " + msg.decode())
                f_ctrlr.delete_file(self.connection, msg)

        #request = self.parse_request(raw_request.decode())
        #self.process_request(request)
        else:
            print("Empty request body")
        self.connection.close()
        connections.remove(self.connection)

    def process_request(self, request):
        if "query" not in request:
            raise RuntimeError("request is missing query field")
        else:
            print("searching for {} in Knowledge Base".format(request["query"]))

    def parse_request(self, request):
        """ Parse incoming request string and return each key, value pair as a native python dictionary. """
        return {key : val for (key, val) in (entry.split(":") for entry in request.split(";"))}
