from . import db
from . import SUCCESS, FAILURE

def login_user(connection, login_info):
    print("Inside login")
    username = login_info['username']
    password = login_info['password']
    if db.login(username, password):
        connection.send(SUCCESS)
    else:
        connection.send(FAILURE)



def register_user(register_info):
    print("Inside RegisterHandler")
    username = register_info['username']
    password = register_info['password']
    print("Leaving RegisterHandler")
    return db.register(username, password)
