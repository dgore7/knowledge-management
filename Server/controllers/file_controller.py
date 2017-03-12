from Server import verboseFunc
from . import db, SOCKET_EOF
import os

import os
import pickle
from . import db, SUCCESS, FAILURE

@verboseFunc
def upload_file(connection, upload_info):
    """
    upload a user's file to the database

    :param connection: client connection
    :type socket.socket:
    :param upload_info: file info (i.e. name and tags)
    :type upload_info: dict
    """

    filename = upload_info['fname']
    tags = [tag.strip() for tag in upload_info['tags'].split(',')]
    group_id = int(upload_info['gid'])
    notes = upload_info['notes']
    mod_time = float(upload_info['mod_time'])
    owner = db.get_username(group_id)
    db.upload(filename, tags, owner, group_id, notes, mod_time)

    if  db.__contains__(filename,owner):
        connection.send(FAILURE + "ERROR: file already exists".encode())
    else:
        connection.send(SUCCESS)
    prefix = 'FILE_REPO'
    repo_name = db.repo_name(group_id)
    if not repo_name:
        print('REPO NAME ERROR')
        return
    file = open(os.path.normpath(
        os.path.join(
            os.getcwd(),
            prefix,
            repo_name,
            filename)), 'wb')
    print("\tOpened file: " + filename)
    # date_time_info = connection.recv(1024)
    #
    # print(date_time_info)
    #
    # print("File receieved. Sending response.")
    #
    # connection.send("SUCCESS".encode())
    #
    # months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # file_metadata = date_time_info.decode().split("|")
    #
    # month = months[int(file_metadata[1]) - 1]
    # print(file_metadata[0] + " " + month)

    while True:
        line = connection.recv(1024)
        print(line)
        if line == SOCKET_EOF:
            break
        else:
            file.write(line)

    file.close()
    print("Closed File")


@verboseFunc
def retrieve_file(connection, filename):

    print("Inside RetrieveHandler")
    print(filename.decode())
    file = open(filename, 'rb')

    for line in file:
        connection.send(line)

    print("\tOpened file: " + filename.decode())

    file.close()
    print("Leaving RetrieveHandler")


@verboseFunc
def retrieve_repo(connection, query):
    if 'group_id' not in query:
        connection.send(FAILURE)
    try:
        group_id = query['group_id']
    except KeyError as e:
        msg = ','.join(arg for arg in e.args).encode()
        connection.send(FAILURE + msg)
        return
    connection.send(SUCCESS)
    repo = db.retrieve_repo(group_id)
    pickled_repo = pickle.dumps(repo)
    connection.send(pickled_repo)


@verboseFunc
def retrieve_personal_repo(connection, uname):
    repo_id = db.get_personal_repo_id(uname)
    retrieve_repo(connection, {'group_id': repo_id})


@verboseFunc
def delete_file(connection, query):
    print("Inside DeleteHandler")
    if 'filename' not in query or 'group_id' not in query:
        connection.send(connection.send(FAILURE + " ERROR: missing parameters".encode()))
    filename = query['filename']
    group_id = query['group_id']
    if db.delete(filename, group_id):
        connection.send(SUCCESS)
    else:
        connection.send(FAILURE + " ERROR: deletion failed".encode())
    print("Leaving DeleteHandler")
