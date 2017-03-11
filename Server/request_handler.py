import threading

import struct

from Server import connections
from socket import SHUT_WR, error as SocketError, errno as SocketErrno

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
            try:
                raw_request = self.connection.recv(2048)
                print(raw_request.decode())

                if len(raw_request):
                    client_option = raw_request.decode()
                    print("CO: " + client_option)

                    if client_option == "login":
                        print("SENDING OK MESSAGE!")
                        self.connection.send(SUCCESS)
                        msg = self.connection.recv(1024)
                        login_info = self.parse_request(msg.decode())
                        print("Logging in with: " + msg.decode())
                        repo_id = u_ctrlr.login_user(self.connection, login_info)
                        if not repo_id:
                            self.connection.send(FAILURE)
                        else:
                            self.connection.send(SUCCESS)
                            packed_repo_id = struct.pack('<L', repo_id)
                            self.connection.send(packed_repo_id)

                    elif client_option == "register":
                        msg = self.connection.recv(1024).decode()
                        print("Registering user: " + msg)
                        repo_id = u_ctrlr.register_user(self.parse_request(msg))
                        print(repo_id)
                        if repo_id:
                            self.connection.send(SUCCESS)
                            packed_repo_id = struct.pack('<L', repo_id)
                            self.connection.send(packed_repo_id)
                            print("Successfully registered user: " + msg)
                        else:
                            self.connection.send(FAILURE)
                            print("Failed to register user: " + msg)

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

                    elif client_option == "addMemGrp":
                        print("NEED TO IMPLEMENT SERVER SIDE MEMBER ADD TO GROUP HANDLER!")
                        self.connection.send(FAILURE)

                    elif client_option == "removeMemGrp":
                        print("NEED TO IMPLEMENT SERVER SIDE MEMBER REMOVE FROM GROUP HANDLER!")
                        self.connection.send(FAILURE)

                    else:
                        self.connection.send(FAILURE)

                #request = self.parse_request(raw_request.decode())
                #self.process_request(request)
                else:
                    print("Empty request body")
                    connections.remove(self.connection)
                    try:
                        self.connection.shutdown(SHUT_WR)
                        self.connection.close()
                    except OSError as e:
                        if e.args[0] == 57:
                            print("Connection was already closed!")

                    self.connected = False
                    print("Disconnected from the client!")
                #self.connection.close()
                #connections.remove(self.connection)
            except SocketError as e:
                print("Benign error thrown as request handler was shutdown")
                self.connected = False

    def process_request(self, request):
        if "query" not in request:
            raise RuntimeError("request is missing query field")
        else:
            print("searching for {} in Knowledge Base".format(request["query"]))

    def parse_request(self, request):
        """ Parse incoming request string and return each key, value pair as a native python dictionary. """
        return {key : val for (key, val) in (entry.split(":") for entry in request.split(";"))}
