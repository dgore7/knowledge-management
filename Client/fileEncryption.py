# Encryption class for encrypting files

import os
import random
import struct
from Crypto.Cipher import AES
import binascii
from base64 import b64encode


class fileEncoding:
    def __init__(self, filename):
        self.filename = self.encryptFile(filename)

    def getEncryptedFile(self):
        return self.filename

    def getKey(self):
        return self.key

    def encryptFile(self, filename):
        blocksize = 64 * 1024
        self.key = os.urandom(16)
        encryptedFile = filename + '.enc'

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        cipher = AES.new('This is my key12', AES.MODE_CBC, iv)
        # self.key = binascii.hexlify(self.key)
        self.key = b64encode(self.key).decode('utf-8')
        fileSize = os.path.getsize(filename)

        inputFile = open(filename, 'rb')
        outputFile = open(encryptedFile, 'wb')
        outputFile.write(struct.pack('<Q', fileSize))
        outputFile.write(iv)

        while len(inputFile.read(blocksize)) > 0:
            block = inputFile.read(blocksize)
            if len(block) == 0:
                break
            if len(block) % 16 != 0:
                block += ' ' * (16 - len(block) % 16)

            outputFile.write(cipher.encrypt(block))


a = fileEncoding("encrypt.txt")
print(a.getKey())
