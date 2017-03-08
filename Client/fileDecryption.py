# Decryption class for decrypting a file 

import os
import random
import struct
from Crypto.Cipher import AES


class fileDecoding:
    def __init__(self, filename, key):
        self.filename = self.decryptFile(key, filename)
        self.key = key

    def getDecryptedFile(self):
        return self.filename

    def decryptFile(self, key, encryptedFile, decryptedFile=None):
        blocksize = 24 * 1024

        # if decryptedFile name not specified, automatically sets file name to encrytedFile name without the .enc extension

        if not decryptedFile:
            decryptedFile = os.path.splitext(encryptedFile)[0]

        inputFile = open(encryptedFile, "rb")
        size = struct.unpack('<Q', inputFile.read(struct.calcsize('Q')))[0]
        iv = inputFile.read(16)
        decrypt = AES.new('This is my key12', AES.MODE_CBC, iv)

        # outputFile = open(decryptedFile, "wb")
        # print(len(inputFile.read(blocksize)))
        # while len(inputFile.read(blocksize)) > 0:
        # 	block = inputFile.read(blocksize)
        # 	print(block)
        # 	if len(block) == 0:
        # 		break
        # 	decryptedString = decrypt.decrypt(block)
        # 	print(decryptedString)
        # 	outputFile.write(decryptedString)

        outputFile = open(decryptedFile, 'wb')

        while True:
            block = inputFile.read(blocksize)
            if len(block) == 0:
                break
            outfile.write(decrypt.decrypt(block))

        outputFile.truncate(size)


a = fileDecoding("encrypt.txt.enc", "NDEnc7GpyHHqOJ40nZv0yA==")
