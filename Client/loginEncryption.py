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

	def loginEncryption (self, username):

		# block size for cipher object (always 16 for AES)
		blockSize = 16 

		# padding to ensure that value you encrpyt is a multiple of block size in length 
		padding = "{"

		# pad the text to be encrypted 
		padTheText = lambda s: s + (blockSize - len(s) % blockSize) * padding

		encodeAES = lambda c, s: base64.b64encode(c.encrypt(padTheText(s)))

		# creates a random secret key 
		secretKey = os.urandom(blockSize)

		# cipher object using the secrey key
		cipher = AES.new(secretKey)

		# encrypts username 
		encodedUsername = encodeAES(cipher, username) 

		return encodedUsername

	# def loginDecryption(self, encodedUsername):

	# 	# padding = "{"

	# 	decodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(padding)

	# 	cipher = AES.new(secretkey)

	# 	decodedUsername = decodeAES(cipher, encodedUsername)

	# 	print(decodedUsername)


	# call this when user is registering and creating their password 
	def passwordHashing(self, username, password):
		# uses the username as salt 
		usernameSalt = username

		# adds to the username to make a more secure salt 
		salt = usernameSalt + 'This is CSC 376'

		# store randomSalt with user login info - each user has own random salt
		randomSalt = os.urandom(32)
		finalSalt = randomSalt + salt 
		iterations = 22000

		hex = hashlib.pbkdf2_hmac('sha512', password, salt, iterations, 128)
		hashHex = binascii.hexlify(hex)

		return hashHex
		

a = LoginEncoding("jessicahua95", "hello")

print(a.getUsername())
print(a.getPassword())

















