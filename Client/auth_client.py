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
# https://github.com/beefjerky/new_airflow/blob/6cb785c8a97829833db5293ad3458dd16fcbf68c/airflow/api/auth/backend/kerberos_auth.py
#https://github.com/modauthgssapi/mod_auth_gssapi/tree/912738edbf248c9d9c2960cd4ff1daaa855e6c7e
import sys
import hashlib
import tkinter
import getpass
import paramiko
from Server.models import db

from Client import gui




def main():
    StorePassword("jasmine", "ABC123456789!")

if __name__ == "__main__": main()