from . import db


def login_user(login_info):
    print("Inside login")
    client_information = parse_client_information(login_info)
    if db.login(client_information[0], client_information[1]):
        print("Leaving LoginHandler")
        return True
    else:
        print("Leaving LoginHandler")
        return False



def register_user(register_info):
    print("Inside RegisterHandler")
    client_information = parse_client_information(register_info)

    print("Leaving RegisterHandler")


def parse_client_information(client_info):
    print("Parsed Client Info " + client_info.decode() +
          " -> Username: " + client_info.decode().split(":")[0] +
          " Password: " + client_info.decode().split(":")[1])
    return client_info.decode().split(":")