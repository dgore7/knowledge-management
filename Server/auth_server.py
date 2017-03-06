from Server.models import db


def PasswordRequest(username,password):
    pass_try = 0
    x = 3
    while pass_try < x:
        if ((db.DB.login(username, password))==False):
            pass_try += 1
            print('Incorrect Password, ' + str(x - pass_try) + ' more attempts left\n')
        else:
            pass_try = x + 1

    if pass_try == x and ((db.DB.login(username, password))==False):
        sys.exit('Incorrect Password!')

def StorePassword(username,password):
    pass