# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

"""Accepts incoming client connections, then assigns each client a data_retriever"""

import socket
from data_retriever import DataRetriever

if __name__ == "__main__":
    host = 'localhost'
    port = 8787

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    print('server side')

    # accept up to 10 clients at a time
    s.listen(10)
    while True:
        # sock is new socket, talks to the connected client socket
        sock, address = s.accept()
        print (address)

        # start new thread
        DataRetriever(sock).start()
