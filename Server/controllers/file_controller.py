from . import db
import os


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

    path = file_info[0].split("/")
    filename = path[-1]
    tag = file_info[1]
    comment = file_info[2]
    if filename in db:
        connection.send("FAILURE: file already exists".encode())
    else:
        connection.send("SUCCESS".encode())

    file = open(filename, 'wb')
    print("\tOpened file: " + filename)
    print("\tTag Received: " + tag)
    print("\tComment Received: " + comment)

    date_time_info = connection.recv(1024)

    print(date_time_info)

    print("File receieved. Sending response.")

    connection.send("SUCCESS".encode())

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    file_metadata = date_time_info.decode().split("|")

    month = months[int(file_metadata[1]) - 1]
    print(file_metadata[0] + " " + month)

    while True:
        line = connection.recv(1024)

        if not len(line):
            break
        else:
            file.write(line)

    file.close()
    print("Closed File")
    print("Leaving Upload Handler")

def download_file(connection, filename):
    print("Inside RetrieveHandler")
    print(filename.decode())
    file = open(filename, 'rb')

    for line in file:
        connection.send(line)

    print("\tOpened file: " + filename.decode())

    file.close()
    print("Leaving RetrieveHandler")


# def search_file(filename):
#     print("Inside SearchHandler")
#     print(filename.decode())
#     print("Leaving SearchHandler")

def delete_file(connection, filename):
    print("Inside DeleteHandler")
    print(filename.decode())
    os.remove(filename.decode())
    print("Successfully deleted file")
    connection.send("SUCCESS".encode())
    print("Leaving DeleteHandler")
