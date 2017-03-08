import os
import socket
import atexit
from Server.request_handler import RequestHandler
from Server import connections

import ssl
from OpenSSL import crypto
from os.path import exists, join
import threading


class Server(threading.Thread):
    def __init__(self, gui):
        super(Server, self).__init__()
        self._stop = threading.Event()
        self.is_listening=False
        self.gui = gui


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.server_proc = self.create_secure_socket(os.path.normpath(os.path.join(os.getcwd(), '..')), 'localhost', 8001)
        # server = create_socket(sys.argv[1] if len(sys.argv) >= 2 else 8001)
        atexit.register(self.server_shutdown, self.server_proc)
        self.server_proc.listen(10)
        self.server_loop()


    def create_socket(self, port, host='localhost'):
        self.server_proc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_proc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_proc.bind((host, port))
        print("Server started on {}:{}".format(host, port))
        self.is_listening=True
        return self.server_proc


    def create_secure_socket(self, cert_dir, host='localhost', port=8001):
        context = ssl.SSLContext() # Defaults to SSL/TLS support with PROTOCOL_TLS (best for now for compatibility)
        context.verify_mode = ssl.CERT_OPTIONAL # ssl.CERT_REQUIRED is more secure
        context.check_hostname = False # Hostname verification on certs (Dont want for now)
        context.load_default_certs(purpose=ssl.Purpose.CLIENT_AUTH) # Load the public CA certs for the server socket (need CLIENT_AUTH param)
        self.generate_server_self_cert(cert_dir)
        context.load_cert_chain(join(cert_dir, "KnowledgeManagement.crt"), keyfile=join(cert_dir, "KnowledgeManagement.key")) # TODO FIX THE certfile path!!!!!!!!!!
        self.server_proc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_proc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        secureSocket = context.wrap_socket(self.server_proc, server_side=True)
        secureSocket.bind((host, port))
        print("SSL Server started on {}:{}".format(host, port))
        self.is_listening=True
        return secureSocket


    def generate_server_self_cert(self, cert_dir):
        #parameter: cert_dir -> The directory to store the certificates in.

        # Add code to call OpenSSL to generate a certificate for the server to use
        # Might require an import of PyOpenSSL (OpenSSL)

        CERT_FILE = "KnowledgeManagement.crt"
        KEY_FILE = "KnowledgeManagement.key"

        if not exists(join(cert_dir, CERT_FILE)) \
                or not exists(join(cert_dir, KEY_FILE)):
                # create a key pair
            publicKey = crypto.PKey()
            publicKey.generate_key(crypto.TYPE_RSA, 1024)

            # create a self-signed cert
            cert = crypto.X509()
            cert.get_subject().C = self.gui.selfSignedCertCountry
            cert.get_subject().ST = self.gui.selfSignedCertState
            cert.get_subject().L = self.gui.selfSignedCertLocation
            cert.get_subject().O = self.gui.selfSignedCertOrganization
            cert.get_subject().OU = self.gui.selfSignedCertOrganizationU
            cert.get_subject().CN = socket.gethostname()
            cert.set_serial_number(1000)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(10*365*24*60*60)
            cert.set_issuer(cert.get_subject())
            cert.set_pubkey(publicKey)
            cert.sign(publicKey, 'sha1') # SHA1 has known theoretical attack to produce collisions!

            open(join(cert_dir, CERT_FILE), "wb").write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            open(join(cert_dir, KEY_FILE), "wb").write(
                crypto.dump_privatekey(crypto.FILETYPE_PEM, publicKey))

        else:
            print("Certificate/Key already exist! A new pair will not be generated.")


    def server_loop(self):
        while self.is_listening:
            try:
                sock, addr = self.server_proc.accept()
                print("Recieved new connection from {}.".format(addr))
                connections.append(sock)
                handler = RequestHandler(sock)
                handler.start()
            except socket.error:
                print("Benign connection abort error thrown.")
                break;

    def server_start(self, cert_dir):
        self.server_proc = self.create_secure_socket(cert_dir, 'localhost', 8001)
        # server = create_socket(sys.argv[1] if len(sys.argv) >= 2 else 8001)
        atexit.register(self.server_shutdown, self.server_proc)
        self.server_proc.listen(10)
        self.server_loop()


    def server_shutdown(self):
        self.is_listening = False
        for c in connections:
            c.close()
        try:
            self.server_proc.shutdown(socket.SHUT_WR)
        except OSError as e1:
            if e1.args[0] == 57:
                print("No clients connected?")

        self.server_proc.close()

    def is_listening(self):
        return self.is_listening