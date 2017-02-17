import threading
import time
from server_globals import connections

from upload_handler import UploadHandler
from retrieve_handler import  RetrieveHandler
from login_handler import LoginHandler
from register_handler import RegisterHandler
from search_handler import SearchHandler
from delete_handler import DeleteHandler

class RequestHandler(threading.Thread):
    """ A request handler class which runs in it's own thread """
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection


    def run(self):
        lock = threading.Lock()
        while True:
            raw_request = self.connection.recv(2048)
            if len(raw_request):
                client_option = raw_request.decode()

                if client_option == "login":
                    msg = self.connection.recv(1024)
                    print("Logging in with: " + msg.decode())
                    LoginHandler(msg)

                elif client_option == "register":
                    msg = self.connection.recv(1024)
                    print("Registering user: " + msg.decode())
                    RegisterHandler(msg)

                elif client_option == "upload":
                    msg = self.connection.recv(1024)
                    print ("Received: " + msg.decode() )
                    UploadHandler(self.connection, msg, lock).start()
                    time.sleep(2)

                elif client_option == "retrieve":
                    msg = self.connection.recv(1024)
                    print("Retrieving File: " + msg.decode())
                    RetrieveHandler(msg)

                elif client_option == "search":
                    msg = self.connection.recv(1024)
                    print("Searching for: " + msg.decode())
                    SearchHandler(msg)

                elif client_option == "delete":
                    msg = self.connection.recv(1024)
                    print("Deleting file: " + msg.decode())
                    DeleteHandler(msg)

            #request = self.parse_request(raw_request.decode())
            #self.process_request(request)
            else:
                print("Empty request body")
                self.connection.close()
                connections.remove(self.connection)
                return

    def process_request(self, request):
        if "query" not in request:
            raise RuntimeError("request is missing query field")
        else:
            print("searching for {} in Knowledge Base".format(request["query"]))

    def parse_request(self, request):
        """ Parse incoming request string and return each key, value pair as a native python dictionary. """
        return {key : val for (key, val) in (entry.split(":") for entry in request.split(";"))}