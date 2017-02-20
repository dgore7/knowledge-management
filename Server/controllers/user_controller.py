import hashlib

def login_user(login_info):
    print("Inside login")
<<<<<<< HEAD
    print("Extra line")
    print(login_info.decode())
=======
    login_info_list = login_info.decode().split(':')
    print("Username: " + login_info_list[0] + " | " + "Password: " + login_info_list[1])
    print("Username: " + login_info_list[0] + " | " + "Hashed Password: " + hashlib.sha3_512(login_info_list[1].encode()).hexdigest())
    # Add input sanitation code for username

    # Need to call DB functions here
>>>>>>> origin/feature/auth
    print("Leaving LoginHandler")

def register_user(register_info):
    print("Inside RegisterHandler")
    print(register_info.decode())
    print("Leaving RegisterHandler")