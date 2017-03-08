# Encryption class for encrypting login info 

from Crypto.Cipher import AES
import base64
import os
import hashlib
import binascii


class LoginEncoding:
    def __init__(self, username, password):
        self.username = self.loginEncryption(username)
        self.password = self.passwordHashing(username, password)

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getUserKey(self):
        return self.key

    def getPasswordSalt(self):
        return self.salt

    def loginEncryption(self, username):
        # block size for cipher object (always 16 for AES)
        blockSize = 16

        # padding to ensure that value you encrpyt is a multiple of block size in length
        padding = "{"

        # pad the text to be encrypted
        padTheText = lambda s: s + (blockSize - len(s) % blockSize) * padding

        encodeAES = lambda c, s: base64.b64encode(c.encrypt(padTheText(s)))

        # creates a random secret key
        self.key = os.urandom(blockSize)

        # cipher object using the secrey key
        cipher = AES.new(self.key)

        # encrypts username
        encodedUsername = encodeAES(cipher, username)

        return encodedUsername


    def loginDecryption(self, key, encodedUsername):
        mode = 'utf-8'

        padding = "{"

        blockSize = 16

        padTheText = lambda s: s + (blockSize - len(s) % blockSize) * padding

        decodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

        cipher = AES.new(key)

        decodedUsername = decodeAES(cipher, encodedUsername)

        decodedUsername = str(decodedUsername, mode)

        decodedUsername = decodedUsername.rstrip(padding)

        return decodedUsername

    # call this when user is registering and creating their password
    def passwordHashing(self, username, password):
        # uses the username as salt
        usernameSalt = username

        # adds to the username to make a more secure salt
        salt = usernameSalt + 'This is CSC 376'

        salt = str.encode(salt)
        # store randomSalt with user login info - each user has own random salt
        randomSalt = os.urandom(32)

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


a = LoginEncoding("jessicahua95", "hello")

print(a.getUsername())
print(a.loginDecryption(a.getUserKey(), a.getUsername()))
print(a.getPassword())
