import sys
import socket
from Server.request_handler import RequestHandler
from Server import connections

import ssl
import OpenSSL

def create_socket(port, host='localhost'):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    print("Server started on {}:{}".format(host, port))
    return server

def create_secure_socket(port, host='localhost', cert_dir):
    context = ssl.SSLContext() # Defaults to SSL/TLS support
    context.verify_mode = ssl.CERT_OPTIONAL # ssl.CERT_REQUIRED is more secure
    context.check_hostname = False # Hostname verification on certs (Dont want for now)
    context.load_default_certs(purpose=Purpose.CLIENT_AUTH) # Load the public CA certs for the server socket (need CLIENT_AUTH param)
    context.load_cert_chain(certfilePath, keyfile=keyfilePath) # TODO FIX THE certfile path!!!!!!!!!!
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    secureSocket = context.wrap_socket(server, server_side = True)
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

        open(join(cert_dir, CERT_FILE), "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wt").write(
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

        

if __name__ == '__main__':
    server = create_socket(sys.argv[1] if len(sys.argv) >= 2 else 8001)
    server.listen(10)
    server_loop(server)