import threading
import time
from Server import connections

from Server.controllers import file_controller as f_ctrlr, user_controller as u_ctrlr


class RequestHandler(threading.Thread):
    """ A request handler class which runs in it's own thread """
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        connections.append(self.connection)
        print("Connection made")


    def run(self):
        raw_request = self.connection.recv(2048)
        print(raw_request.decode())
        if len(raw_request):
            client_option = raw_request.decode()

            if client_option == "login":
                msg = self.connection.recv(1024)
                print("Logging in with: " + msg.decode())
                u_ctrlr.login_user(msg)

            elif client_option == "register":
                msg = self.connection.recv(1024)
                print("Registering user: " + msg.decode())
                u_ctrlr.register_user(msg)

            elif client_option == "upload":
                self.connection.send("OK".encode())
                msg = self.connection.recv(1024)
                print ("Received: " + msg.decode() )
                f_ctrlr.upload_file(self.connection, msg)

            elif client_option == "retrieve":
                msg = self.connection.recv(1024)
                print("Retrieving File: " + msg.decode())
                f_ctrlr.retrieve_file(msg)

            elif client_option == "search":
                msg = self.connection.recv(1024)
                print("Searching for: " + msg.decode())
                f_ctrlr.search_file(msg)

            elif client_option == "delete":
                msg = self.connection.recv(1024)
                print("Deleting file: " + msg.decode())
                f_ctrlr.delete_file(msg)

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