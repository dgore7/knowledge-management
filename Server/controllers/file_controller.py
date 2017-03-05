import os
import pickle
from . import db, SUCCESS, FAILURE


def upload_file(connection, upload_info):
    """
    upload a user's file to the database

    :param connection: client connection
    :type socket.socket:
    :param upload_info: file info (i.e. name and tags)
    :type upload_info: dict
    """
    print("Inside Upload Handler")

    filename = upload_info['fname']
    tags = [tag.strip() for tag in upload_info['tags'].split(',')]
    owner = upload_info['gid']
    group_id = upload_info['gid']
    db.upload(filename, tags, owner, group_id)

    if filename in db:
        connection.send(FAILURE + "ERROR: file already exists".encode())
    else:
        connection.send(SUCCESS)
    prefix = os.path.normpath('../FILE_REPO/')
    file = open(os.path.normpath(os.path.join(os.getcwd(), prefix, filename)), 'wb')
    print("\tOpened file: " + filename)

    while True:
        line = connection.recv(1024)
        print(line)
        if not len(line):
            break
        else:
            file.write(line)

    file.close()
    print("Closed File")
    print("Leaving Upload Handler")


def retrieve_file(filename):
    print("Inside RetrieveHandler")
    print(filename.decode())
    print("Leaving RetrieveHandler")


def retrieve_repo(connection, query):
    if 'group_id' not in query:
        connection.send(FAILURE)
    try:
        group_id = query['group_id']
    except KeyError as e:
        msg = ','.join(arg for arg in e.args).encode()
        connection.send(FAILURE + msg)
    connection.send(SUCCESS)
    repo = db.retrieve_repo(group_id)
    pickled_repo = pickle.dumps(repo)
    connection.send(pickled_repo)


def retrieve_personal_repo(connection, uname):
    repo_id = db.get_personal_repo_id(uname)
    retrieve_repo(connection, repo_id)


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
