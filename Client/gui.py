#from client import Client

import tkinter as tk

import start
import login
import register
import menu
import upload
import retrieve
import search
import delete
import group
import group_management

from client import Client


class GUI(tk.Tk):
	#Inherites tkinter class
	def __init__(self, user):
		#parameter: user -> A Client object

		"""
		Binds the GUI to a Client object. 
		"""
		self.user = user

		"""
		Initializes a tkinter object
		"""
		tk.Tk.__init__(self)

		"""
		Changes the title of the window
		"""
		tk.Tk.wm_title(self, "Knowledge Management")

		"""
		Creates a tkinter Frame and packs it
		"""
		window = tk.Frame(self)
		window.pack(side="top", fill="both", expand="True")
		window.grid_rowconfigure(0, weight=1)

		window.grid_columnconfigure(0, weight=1)

		"""
		A dictionary of frames. Used to change display between windows.
		"""
		self.frames = {}

		"""
		Creates multiple frames using the window frame 
		and stores each of them into the frames dictionary.
		"""
		for F in (start.StartPage, login.LoginPage, register.RegisterPage, menu.MenuPage,
			upload.UploadPage, retrieve.RetrievePage, search.SearchPage, delete.DeletePage,
		    group.GroupPage, group_management.GroupManagementPage):
			frame = F(window, self)
			self.frames[F] = frame
			frame.grid(row = 0, sticky = "nsew")

		"""
		Displays the starting frame
		"""
		self.show_frame(start.StartPage)

	def show_frame(self, display):
		#parameter: display -> The frame that is too be display

		"""
		Chooses the frame from the dictionary and displays it on the window.
		"""
		frame = self.frames[display]
		frame.tkraise()

	def getClient(self):
		return self.user

if __name__ == '__main__':
	user = Client()
	app = GUI(user)
	app.geometry("600x500")
	app.mainloop()
	user.disconnect()