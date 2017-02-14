import threading
from server_globals import connections


class RequestHandler(threading.Thread):
    """ A request handler class which runs in it's own thread """
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        raw_request = self.connection.recv(2048)
        if len(raw_request):
            request = self.parse_request(raw_request.decode())
            self.process_request(request)
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