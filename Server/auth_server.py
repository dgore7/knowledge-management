from Server.controllers import user_controller
import sys

class SeverAuth():

    def PasswordRequest(username,password): #have to change to take login info variable
        'Will lock user out of application for duration after 3 failed attempts'
        pass_try = 0
        x = 3
        while pass_try < x:
            if ((user_controller.login_user(username, password))==False):
                pass_try += 1
                print('Incorrect Password, ' + str(x - pass_try) + ' more attempts left\n')
            else:
                pass_try = x + 1

        if pass_try == x and ((user_controller.login_user(username, password))==False):
            sys.exit('Incorrect Password!')

    def StorePassword(username,password):
        pass