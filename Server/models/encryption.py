from Crypto.Cipher import AES
import base64
import os

class encryption:
    def __init__(self):
        pass

    def loginEncryption(self, username):
        # block size for cipher object (always 16 for AES)
        blockSize = 16
        # padding to ensure that value you encrpyt is a multiple of block size in length
        padding = "{"
        # pad the text to be encrypted
        padTheText = lambda s: s + (blockSize - len(s) % blockSize) * padding
        # encrypt with AES, encode with base 64
        encodeAES = lambda c, s: base64.b64encode(c.encrypt(padTheText(s)))
        # creates a random secret key
        secretKey = os.urandom(blockSize)
        # cipher object using the secrey key
        cipher = AES.new(secretKey)
        # encrypts username
        encodedUsername = encodeAES(cipher, username)
        print(encodedUsername)