import tkinter as tk

from Server import server
from Server import home_gui
from Server import settings_gui
from Server import about_gui


class GUI(tk.Tk):
	#Inherites tkinter class
	def __init__(self):
		# Sets the certificate settings for the self signed cert
		self.selfSignedCertCountry = "US"
		self.selfSignedCertState = "Illinois"
		self.selfSignedCertLocation = "Chicago"
		self.selfSignedCertOrganization = "CSC 376 - Distributed Systems"
		self.selfSignedCertOrganizationU = "Knowledge Mangement Group"

		"""
		Initializes a tkinter object
		"""
		tk.Tk.__init__(self)

		"""
		Changes the title of the window
		"""
		tk.Tk.wm_title(self, "Knowledge Management Server Manager")

		mainServerMenu = tk.Menu(self)
		self.config(menu=mainServerMenu)

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
        Creates multiple frames using the window frame
        and stores each of them into the frames dictionary.
        """
		for F in (home_gui.HomePage, settings_gui.SettingsPage, about_gui.AboutPage):
			frame = F(window, self)
			self.frames[F] = frame
			frame.grid(row=0, sticky="nsew")

		"""
					Last menu item which has the about window, help, etc
		"""

		thisgui = self
		helpMenu = tk.Menu(self)
		mainServerMenu.add_cascade(label="Help", menu=helpMenu)
		helpMenu.add_command(label="About", command=thisgui.show_frame(about_gui.AboutPage))


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
	app.geometry("700x200")
	app.mainloop()
	# Method to see if the server is currently running
	#if self.server.is_listening():
		#self.server.server_shutdown()