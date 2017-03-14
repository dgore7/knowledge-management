from Server.controllers import user_controller
import sys

class SeverAuth():

    def PasswordAttempts(connection, login_info): #have to change to take login info variable
        'Will lock user out of application for duration after 3 failed attempts'
        pass_try = 0
        x = 3
        password = login_info["password"]
        username = login_info["username"]
        while pass_try < x:
            if ((user_controller.login_user(username, password))==False):
                pass_try += 1

                connection.send
                print()
            else:
                pass_try = x + 1

        if pass_try == x and ((user_controller.login_user(username, password))==False):
            sys.exit('Incorrect Password!')

    def StorePassword(username,password):
        pass