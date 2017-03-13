# Encryption class for encrypting login info
# 81 lines
from Crypto.Cipher import AES
import base64
import os
import hashlib
import binascii
import time
from itertools import zip_longest


class LoginEncoding:
    def __init__(self):
        self.username = ''
        self.usernamePlain = ''
        self.password = ''
        self.key = ''
        self.salt = ''
        self.dateTime = time.strftime("%I:%M:%S")

    def setUsername(self, username):
        if len(username) == 0:
            print('The username passed in is empty or null!')

        self.usernamePlain = username
        encryptedUsername = self.loginEncryption(self.usernamePlain)
        self.username = encryptedUsername

    def setPassword(self, password):
        self.errorCheckPassword(password)

        hashedPassword = self.passwordHashing(self.usernamePlain, password, '')
        self.password = hashedPassword

    def setPasswordWithSalt(self, password, salt):
        self.errorCheckPassword(password)

        hashedPassword = self.passwordHashing(self.usernamePlain, password, salt)
        self.password = hashedPassword

    def errorCheckPassword(self, password):
        if len(password) == 0:
            print('The pasword passed in is empty or null!')

    def getUsername(self):
        mode = 'utf-8'
        usernameString = str(self.username, mode)
        return usernameString

    def getPassword(self):
        mode = 'utf-8'
        passwordString = str(self.password, mode)
        return passwordString

    def getUserKey(self):
        return self.key

    def getPasswordSalt(self):
        return self.salt

    def getDateTime(self):
        return self.dateTime

    def loginEncryption(self, username):
        # block size for cipher object (always 16 for AES)
        blockSize = 16

        # padding to ensure that value you encrpyt is a multiple of block size in length
        padding = "{"

        # pad the text to be encrypted
        padTheText = lambda s: s + (blockSize - len(s) % blockSize) * padding

        encodeAES = lambda c, s: base64.b64encode(c.encrypt(padTheText(s)))

        # creates a random secret key
        self.key = 'This is a username secret key12.'

        # cipher object using the secrey key
        cipher = AES.new(self.key)

        # encrypts username
        encodedUsername = encodeAES(cipher, username)

        return encodedUsername

    def loginDecryption(self, encodedUsername):
        mode = 'utf-8'

        padding = "{"

        blockSize = 16

        padTheText = lambda s: s + (blockSize - len(s) % blockSize) * padding

        decodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

        cipher = AES.new('This is a username secret key12.')

        decodedUsername = decodeAES(cipher, encodedUsername)

        decodedUsername = str(decodedUsername, mode)

        decodedUsername = decodedUsername.rstrip(padding)

        return decodedUsername

    # call this when user is registering and creating their password
    def passwordHashing(self, username, password, saltDB):
        mode = 'utf-8'
        # uses the username as salt
        usernameSalt = username

        # adds to the username to make a more secure salt
        salt = usernameSalt + 'This is CSC 376'

        salt = str.encode(salt)
        # store randomSalt with user login info - each user has own random salt
        randomSalt = ''
        if saltDB == '':
            randomSalt = os.urandom(32)
        else:
            randomSalt = saltDB

        finalSalt = randomSalt + salt

        self.salt = finalSalt

        iterations = 22000

        password = str.encode(password)

        hex = hashlib.pbkdf2_hmac(hash_name='sha256',
                                  password=password,
                                  salt=finalSalt,
                                  iterations=iterations,
                                  dklen=128)

        hashHex = binascii.hexlify(hex)

        return hashHex

    def checkPassword(self):
        rightPass = self.getPassword()
        attemptPass = self.getPassword()

        if len(rightPass) == 0:
            print('The password from database is empty or null!')

        if len(attemptPass) == 0:
            print('The password entered is empty or null!')

        assert len(rightPass) == len(attemptPass)

        difference = False

        rightPassArray = list(rightPass)
        attemptPassArray = list(attemptPass)

        assert len(rightPassArray) == len(attemptPassArray)

        arrayLength = len(rightPassArray)
        for index in range(arrayLength - 1):
            compare = rightPassArray[index] == attemptPassArray[index]
            difference |= compare

        return difference


a = LoginEncoding()
a.setUsername("jessicahua95")
a.setPassword("hello")

print("Username: " + a.getUsername())
print(a.loginDecryption(a.getUsername()))
print(a.getPasswordSalt())
print("Password: " + a.getPassword())
print(a.checkPassword())

