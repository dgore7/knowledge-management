# Encryption class for encrypting login info
# 81 lines
#from Crypto.Cipher import AES
import base64
import os
import hashlib
import binascii
import time
from itertools import zip_longest


class LoginEncoding:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.salt = ''
        self.dateTime = time.strftime("%I:%M:%S")

    def setUsername(self, username):
        if len(username) == 0:
            print('The username passed in is empty or null!')

        self.username = username

    def setPassword(self, password):
        self.errorCheckPassword(password)

        hashedPassword = self.passwordHashing(self.username, password)
        self.password = hashedPassword

    def errorCheckPassword(self, password):
        if len(password) == 0:
            print('The password passed in is empty or null!')

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getDateTime(self):
        return self.dateTime


    # call this when user is registering and creating their password
    def passwordHashing(self, username, password):
        mode = 'utf-8'
        # uses the username as salt
        usernameSalt = str(username)

        # adds to the username to make a more secure salt
        salt = usernameSalt + 'This is CSC 376'

        finalSalt = str.encode(salt)
        self.salt = finalSalt

        iterations = 22000

        password = str.encode(password)

        # TODO: Change this to use Argon2 (see argon2 0.1.10 BETA) instead. Far more resistant to GPU and ASIC based attacks.
        hex = hashlib.pbkdf2_hmac(hash_name='sha256',
                                  password=password,
                                  salt=finalSalt,
                                  iterations=iterations,
                                  dklen=128)

        hashHex = str(binascii.hexlify(hex))

        return hashHex


#a = LoginEncoding()
#a.setUsername("jessicahua95")
#a.setPassword("hello")

#print("Username: " + a.getUsername())
#print(a.loginDecryption(a.getUsername()))
#print(a.getPasswordSalt())
#print("Password: " + a.getPassword())
#print(a.checkPassword())

