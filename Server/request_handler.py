import threading
from . import server_globals


class RequestHandler(threading.Thread):
    """ A request handler class which runs in it's own thread """
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        """
        execute the request handler thread
        """
        raw_request = self.connection.recv(2048)
        if len(raw_request):
            request = self.parse_request(raw_request.decode())
            self.process_request(request)
        else:
            print("Empty request body")
            self.connection.close()
            server_globals.connections.remove(self.connection)

    def process_request(self, request):
        """
        process the request and execute the appropriate action
        :param request: a parsed request
        :type request: dict
        """
        if "type" not in request:
            raise RuntimeError("request is missing type field")
        request_type = request["type"]

        print("searching for {} in Knowledge Base".format(request["query"]))


    def parse_request(self, request):
        """ Parse incoming request string and return each key, value pair as a native python dictionary. """
        return {key : val for (key, val) in (entry.split(":") for entry in request.split(";"))}