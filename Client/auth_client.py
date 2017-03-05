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
# https://github.com/celery/py-amqp/blob/787793c66e1027e3cfd5585bfb374e163ec3948c/t/unit/test_sasl.py
# https://github.com/celery/py-amqp/blob/8aa492d96c4a5a6deeb64b852cedd0a38f07b0ee/amqp/sasl.py
# https://github.com/leixiayang/python/blob/17e36833842dd37f8e1f5a7975b818945b3537c8/test/test_auth.py
# https://github.com/ArnaudRemi/spatssh/blob/5ab23f8e38bfb638560500fe81333c57622686d3/spatssh/usr/share/spatssh/Server.py
# https://github.com/ArnaudRemi/spatssh/blob/5ab23f8e38bfb638560500fe81333c57622686d3/spatssh/usr/share/spatssh/Client.py
# Paramiko
#https://github.com/JasonDean-1/TestAutomation/blob/5eff85e2f45170114d327a1cefe020e2d6dc304f/demo_simple.py
import sys
import hashlib
import tkinter
import getpass
import paramiko
from Server.models import db

from Client import gui

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

    password = hashlib.sha224((str(password)).encode('utf-8')).hexdigest()
    try:
        db.DB.register(username, password)
    except:
        sys.exit('Not able to register.')

    print ("Password safely stored in database")

def main():
    StorePassword("jasmine", "ABC123456789!")

if __name__ == "__main__": main()