import os
import socket
import atexit
from Server.request_handler import RequestHandler
from Server import connections

import ssl
from OpenSSL import crypto
from os.path import exists, join


class Server:
    def create_socket(port, host='localhost'):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        print("Server started on {}:{}".format(host, port))
        return server


    def create_secure_socket(cert_dir, host='localhost', port=8001):
        context = ssl.SSLContext() # Defaults to SSL/TLS support with PROTOCOL_TLS (best for now for compatibility)
        context.verify_mode = ssl.CERT_OPTIONAL # ssl.CERT_REQUIRED is more secure
        context.check_hostname = False # Hostname verification on certs (Dont want for now)
        context.load_default_certs(purpose=ssl.Purpose.CLIENT_AUTH) # Load the public CA certs for the server socket (need CLIENT_AUTH param)
        Server.generate_server_self_cert(cert_dir)
        context.load_cert_chain(join(cert_dir, "KnowledgeManagement.crt"), keyfile=join(cert_dir, "KnowledgeManagement.key")) # TODO FIX THE certfile path!!!!!!!!!!
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        secureSocket = context.wrap_socket(server, server_side=True)
        secureSocket.bind((host, port))
        print("SSL Server started on {}:{}".format(host, port))
        return secureSocket


    def generate_server_self_cert(cert_dir):
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
            cert.get_subject().C = "US"
            cert.get_subject().ST = "Illinois"
            cert.get_subject().L = "Chicago"
            cert.get_subject().O = "CSC 376 - Distributed Systems"
            cert.get_subject().OU = "Knowledge Management Group"
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


    def server_loop(server):
        while True:
            sock, addr = server.accept()
            print("Recieved new connection from {}.".format(addr))
            connections.append(sock)
            handler = RequestHandler(sock)
            handler.start()

    def server_start(self, cert_dir):
        server = self.create_secure_socket(cert_dir, 'localhost', 8001)
        # server = create_socket(sys.argv[1] if len(sys.argv) >= 2 else 8001)
        atexit.register(self.server_shutdown, server)
        server.listen(10)
        self.server_loop(server)


    def server_shutdown(server):
        server.close()
        for c in connections:
            c.close()