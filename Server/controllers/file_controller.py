from Server import verboseFunc
from . import db, SOCKET_EOF
import os

import os
import pickle
from . import db, SUCCESS, FAILURE

prefix = 'FILE_REPO'

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
    file_size = int(upload_info['size'])
    if group_id != 0:
        owner = db.get_username(group_id)
    else:
        owner = 'SHARED'
    db.upload(filename, tags, owner, group_id, notes, mod_time, file_size)

    if db.__contains__(filename,owner):
        connection.send(FAILURE + "ERROR: file already exists".encode())
    else:
        connection.send(SUCCESS)

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
def retrieve_file(connection, file_info):

    print("Inside RetrieveHandler")
    filename = file_info['filename']
    gid = file_info['gid']
    repo_name = db.repo_name(gid)
    try:
        file = open(os.path.normpath(
            os.path.join(
                os.getcwd(),
                prefix,
                repo_name,
                filename)), 'rb')
    except FileNotFoundError:
        connection.send(FAILURE)
        return
    connection.send(SUCCESS)

    for line in file:
        connection.send(line)

    print("\tOpened file: " + file.name)
    file.close()
    connection.send(SOCKET_EOF)
    print("Leaving RetrieveHandler")


@verboseFunc
def retrieve_repo(connection, query):
    if 'group_ids' not in query:
        connection.send(FAILURE)
        return
    group_ids = query['group_ids']
    group_ids = group_ids.split(',')
    connection.send(SUCCESS)
    result = []
    for group_id in group_ids:
        result.extend(db.retrieve_repo(int(group_id)))
    pickled_repo = pickle.dumps(result)
    connection.send(pickled_repo)
    connection.send(SOCKET_EOF)


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
