def upload_file(connection, upload_info):
    """
    upload a user's file to the database

    :param connection: client connection
    :type socket.socket:
    :param upload_info: file info (i.e. name and tags)
    :type upload_info: string
    """
    print("Inside Upload Handler")

    file_info = upload_info.decode().split(":")

    filename = file_info[0]

    file = open(filename, 'w')
    print("\tOpened file: " + filename)

    while True:
        line = connection.recv(1024)
        print("\tLine: " + line.decode())

        if line.decode() == '0':
            # file.close()
            break
        else:
            file.write(line.decode())

    file.close()
    print("Closed File")
    print("Leaving Upload Handler")

def retrieve_file(filename):
    print("Inside RetrieveHandler")
    print(filename.decode())
    print("Leaving RetrieveHandler")

def search_file(filename):
    print("Inside SearchHandler")
    print(filename.decode())
    print("Leaving SearchHandler")

def delete_file(filename):
    print("Inside DeleteHandler")
    print(filename.decode())
    print("Leaving DeleteHandler")
