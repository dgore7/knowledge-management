import threading
from Server import connections
from socket import SHUT_RDWR, error as SocketError, errno as SocketErrno

from Server.controllers import SUCCESS, FAILURE, file_controller as f_ctrlr, user_controller as u_ctrlr



class RequestHandler(threading.Thread):
    """ A request handler class which runs in it's own thread """
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        connections.append(self.connection)
        self.connected = True
        print("Connection made")
        self.username = ""

    def run(self):
        while self.connected:
            raw_request = self.connection.recv(2048)
            print(raw_request.decode())

            if len(raw_request):
                client_option = raw_request.decode()
                print("CO: " + client_option)

                if client_option == "login":
                    print("SENDING OK MESSAGE!")
                    self.connection.send(SUCCESS)
                    msg = self.connection.recv(1024).decode()
                    print(msg)
                    login_info = self.parse_request(msg)
                    print("Logging in with: ")
                    u_ctrlr.login_user(self.connection, login_info)

                elif client_option == "register":
                    msg = self.connection.recv(1024).decode()
                    print("Registering user: " + msg)
                    if u_ctrlr.register_user(self.parse_request(msg)):
                        self.connection.send(SUCCESS)
                        print("Successfully registered user: ")
                    else:
                        self.connection.send(FAILURE)
                        print("Failed to register user: ")

                elif client_option == "upload":
                    self.connection.send(SUCCESS)
                    msg = self.connection.recv(1024).decode()
                    print("Received: " + msg)
                    msg = self.parse_request(msg)
                    f_ctrlr.upload_file(self.connection, msg)

                elif client_option == "retrieve":
                    msg = self.connection.recv(1024)
                    print("Retrieving File: " + msg.decode())
                    f_ctrlr.retrieve_file(msg)

                elif client_option == "retrieve_repo":
                    self.connection.send(SUCCESS)
                    msg = self.connection.recv(1024).decode()
                    print("Retrieving File: " + msg)
                    f_ctrlr.retrieve_file(self.parse_request(msg))

                elif client_option == "search":
                    msg = self.connection.recv(1024)
                    print("Searching for: " + msg.decode())
                    f_ctrlr.search_file(msg)

                elif client_option == "delete":
                    self.connection.send(SUCCESS)
                    msg = self.connection.recv(1024).decode()
                    print("Deleting file: " + msg)
                    f_ctrlr.delete_file(self.connection, self.parse_request(msg))

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

                else:
                    self.connection.send(FAILURE)

            #request = self.parse_request(raw_request.decode())
            #self.process_request(request)
            else:
                print("Empty request body")
                connections.remove(self.connection)
                try:
                    self.connection.shutdown(SHUT_RDWR)
                    self.connection.close()
                except OSError as e:
                    if e.args[0] == 57:
                        print("Connection was already closed!")

                self.connected = False
                print("Disconnected from the client!")
            #self.connection.close()
            #connections.remove(self.connection)

    def process_request(self, request):
        if "query" not in request:
            raise RuntimeError("request is missing query field")
        else:
            print("searching for {} in Knowledge Base".format(request["query"]))

    def parse_request(self, request):
        """ Parse incoming request string and return each key, value pair as a native python dictionary. """
        return {key : val for (key, val) in (entry.split(":") for entry in request.split(";"))}
