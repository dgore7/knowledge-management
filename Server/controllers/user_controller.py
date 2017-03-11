from Server import verboseFunc
from . import db
from . import SUCCESS, FAILURE
import os


@verboseFunc
def login_user(connection, login_info):
    username = login_info['username']
    password = login_info['password']
    repo_id = db.login(username, password)
    return repo_id

@verboseFunc
def register_user(register_info):
    username = register_info['username']
    password = register_info['password']
    repo_id = db.register(username, password)
    print(repo_id)
    if repo_id:
        os.makedirs(
            os.path.normpath(
                os.path.join(
                    os.getcwd(),
                    'FILE_REPO',
                    username + '_personal_repo')))
    return repo_id