from . import db


def login_user(login_info):
    print("Inside login")
    username = login_info['username']
    password = login_info['password']
    if db.login(username, password):
        print("Leaving LoginHandler (True)")
        return True
    else:
        print("Leaving LoginHandler (False)")
        return False


def register_user(register_info):
    print("Inside RegisterHandler")
    username = register_info['username']
    password = register_info['password']
    print("Leaving RegisterHandler")
    return db.register(username, password)
