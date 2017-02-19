import threading


class UploadHandler (threading.Thread):
	def __init__(self, connection, upload_info, lock):
		threading.Thread.__init__(self)
		self.connection = connection
		self.upload_info = upload_info
		self.lock = lock

	def run(self):
		print("Inside Upload Handler")

		self.lock.acquire()
		file_info = self.upload_info.decode().split(":")

		filename = file_info[0]

		file = open(filename, 'w')
		print("\tOpened file: " + filename)

		while True:
			line = self.connection.recv(1024)
			print("\tLine: " + line.decode())


			if line.decode() == '0':
				#file.close()
				break
			else:
				file.write(line.decode())

		file.close()
		self.lock.release()

		print("Closed File")

		print("Leaving Upload Handler")