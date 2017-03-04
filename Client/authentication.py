# import pykerberos
# import python-gssapi
#
# class KrbBackend(self):
#
#     def authenticate(self, username=None, password=None):
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD)
#
#

import sys
import hashlib
import getpass
from Client import gui

class Authentication:

    def PasswordRequest(self, gui, password):

        pass_try = 0
        x = 3

        while pass_try < x:
            user_input = input('Please Enter Password: ')
            if user_input != password:
                pass_try += 1
                print ('Incorrect Password, ' + str(x - pass_try) + ' more attempts left\n')
            else:
                pass_try = x + 1

        if pass_try == x and user_input != password:
            sys.exit('Incorrect Password, terminating... \n')
