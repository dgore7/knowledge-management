def login_user(login_info):
    print("Inside login")
    print(login_info.decode())
    print("Leaving LoginHandler")


def register_user(register_info):
    print("Inside RegisterHandler")
    print(register_info.decode())
    print("Leaving RegisterHandler")


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