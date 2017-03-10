from . import db
from . import SUCCESS, FAILURE
import os

def login_user(connection, login_info):
    print("Inside login")
    print(login_info)
    username = login_info['username']
    password = login_info['password']
    repo_id = db.login(username, password)
    if repo_id:
        connection.send(SUCCESS)
        connection.send(str(repo_id).encode())
    else:
        connection.send(FAILURE)

def register_user(register_info):
    print("Inside RegisterHandler")
    username = register_info['username']
    password = register_info['password']
    print("Leaving RegisterHandler")
    if db.register(username, password):
        os.makedirs(
            os.path.normpath(
                os.path.join(
                    os.getcwd(),
                    'FILE_REPO', username + '_personal_repo')))
        return True
    else:
        return False