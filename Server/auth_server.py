__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

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