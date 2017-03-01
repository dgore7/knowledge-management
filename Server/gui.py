import tkinter as tk

from Server import server
from Server import home_gui
from Server import settings_gui


class GUI(tk.Tk):
	#Inherites tkinter class
	def __init__(self):
		#parameter: user -> A Client object


		"""
		Initializes a tkinter object
		"""
		tk.Tk.__init__(self)

		"""
		Changes the title of the window
		"""
		tk.Tk.wm_title(self, "Knowledge Management Server Manager")

		"""
		Creates a tkinter Frame and packs it
		"""
		window = tk.Frame(self)
		window.pack(side="top", fill="both", expand="True")
		window.grid_rowconfigure(0, weight=1)#Who gets prority

		window.grid_columnconfigure(0, weight=1)

		"""
		A dictionary of frames. Used to change display between windows.
		"""
		self.frames = {}

		"""
		Creates multiple frames using the window frame 3
		and stores each of them into the frames dictionary.
		"""
		for F in (home_gui.HomePage, settings_gui.SettingsPage):
			frame = F(window, self)
			self.frames[F] = frame
			frame.grid(row = 0, sticky = "nsew")

		"""
		Displays the starting frame
		"""
		self.show_frame(home_gui.HomePage)

	def show_frame(self, display):
		#parameter: display -> The frame that is too be display

		"""
		Chooses the frame from the dictionary and displays it on the window.
		"""
		frame = self.frames[display]
		frame.tkraise()

	def setServer(self, server):
		"""
			Binds the GUI to a Server object.
		"""
		self.server = server

	def getServer(self):
		return self.server

if __name__ == '__main__':
	#server.start()
	app = GUI()
	app.geometry("400x150")
	app.mainloop()
	# Method to see if the server is currently running
	#if self.server.is_listening():
		#self.server.server_shutdown()