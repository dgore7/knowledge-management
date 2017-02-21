from . import db

def login_user(login_info):
    print("Inside login")
    print("Extra line")
    client_information = login_info.decode().split(":")
    print(client_information)
    username = client_information[0]
    password = client_information[1]
    if db.login(username, password):
        print("Leaving LoginHandler")
        return True
    else:
        print("Leaving LoginHandler")
        return False

def register_user(register_info):
    print("Inside RegisterHandler")
    print(register_info.decode())
    print("Leaving RegisterHandler")