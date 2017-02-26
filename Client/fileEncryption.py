# Encryption class for encrypting files

import os
import random
import struct
from Crypto.Cipher import AES

class fileEncoding: 

	def __init__(self, filename):
		self.filename = self.encryptFile(filename)

	def getEncryptedFile(self):
		return self.filename

	def encryptFile(self, filename): 
		blocksize = 64 * 1024
		key = os.urandom(16)

		encryptedFile = filename + '.enc'

		iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
		cipher = AES.new(key, AES.MODE_CBC, iv)
		fileSize = os.path.getsize(filename)

		inputFile = open(filename, 'r')
		outputFile = open(encryptedFile, 'w')
		outputFile.write(struct.pack('<Q', fileSize))
		outputFile.write(iv)

		while len(inputFile.read(blocksize)) > 0:
			block = inputFile.read(blocksize)
	        if len(block) % 16 != 0:
	            block += ' ' * (16 - len(block) % 16)

	        outputFile.write(cipher.encrypt(block))


a = fileEncoding("encrypt.txt")

