from . import db


def login_user(login_info):
    print("Inside login")
    print(login_info)
    username = login_info['username']
    password = login_info['password']
    if db.login(username, password):
        print("Leaving LoginHandler")
        return True
    else:
        print("Leaving LoginHandler")
        return False


def register_user(register_info):
    print("Inside RegisterHandler")
    username = register_info['username']
    password = register_info['password']
    print("Leaving RegisterHandler")
    return db.register(username, password)



def create_group(group_name, members):
    print("Inside GroupHandler")
    print(group_name.decode())
    print(members)
    print("Leaving GroupHandler")

def add_member(member_name):
    print("Inside AddingHandler")
    print(member_name.decode())
    print("Leaving AddingHandler")

def remove_member(member_name):
    print("Inside RemoveHandler")
    print(member_name.decode())
    print("Leaving RemoveHandler")

