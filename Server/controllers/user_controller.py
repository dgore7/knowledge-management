import hashlib
from . import db

def login_user(login_info):
    print("Inside login")
    login_info_list = login_info.decode().split(':')
    print("Username: " + login_info_list[0] + " | " + "Password: " + login_info_list[1])
    print("Username: " + login_info_list[0] + " | " + "Hashed Password: " + hashlib.sha3_512(login_info_list[1].encode()).hexdigest())
    # TODO: Add input sanitation code for username

    # TODO: Add proper call over to the DB
    return db.login(login_info_list[0], hashlib.sha3_512(login_info_list[1].encode()).hexdigest())


    # Need to call DB functions here
    print("Leaving LoginHandler")

def register_user(register_info):
    print("Inside RegisterHandler")
    print(register_info.decode())
    print("Leaving RegisterHandler")