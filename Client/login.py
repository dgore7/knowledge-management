__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"


import tkinter as tk

from tkinter import TOP, E
import tkinter.messagebox

from Client import gui
from Client import start
from Client import menu

from PIL import ImageTk, Image


class LoginPage(tk.Frame):
	def __init__(self, frame, gui):
		# parameter: frame -> The  frame that will be initalized
		# parameter: gui -> The GUI object that is being used.

		"""
		Initializes the frame that was passed in.
		"""
		tk.Frame.__init__(self, frame)

		"""
		Creates a label to display window name on the screen.
		"""
		label = tk.Label(self, text="Login")
		label.pack(side=TOP)

		# Frame used for organization
		top = tk.Frame(self)
		top.pack(side=TOP)

		# Frame used for organization
		bottom = tk.Frame(self)
		bottom.pack(side=TOP)

		"""
		Creates a label to display 'Username'
		"""
		self.usernameText = tk.Label(top, text="Username")
		self.usernameText.grid(row=0, column=0, sticky=E)

		"""
		Creates a Entry to display a textbox for the client to enter their username.
		"""
		self.usernameInput = tk.Entry(top)
		self.usernameInput.grid(row=0, column=1, sticky=E)

		"""
		Creates a Label to display 'Password'
		"""
		self.passwordText = tk.Label(top, text="Password")
		self.passwordText.grid(row=1, column=0)

		"""
		Creates a Entry to display a textbox for the client to enter their password.
		The text is hidden using '•'.
		"""
		self.passwordInput = tk.Entry(top, show='•')
		self.passwordInput.grid(row=1, column=1)

		"""
		Creates and adds the sign in button.
		Checks if the information provided is valid.
		If valid, takes the client to menu page.
		If not valid, prevents the client from entering.
		"""
		signInButton = tk.Button(bottom, text="Sign-In",
								 command=lambda: self.login(gui, self.usernameInput.get(), self.passwordInput.get()))
		signInButton.grid(row=0)

		"""
		Creates and adds the back button.
		Takes the client back to the starting page when clicked.
		"""
		backButton = tk.Button(bottom, text="Back", command=lambda: self.back(gui))
		backButton.grid(row=0, column=1)

		image = Image.open("penguin.png")
		self.image = Image.composite(image, Image.new('RGB', image.size, 'white'), image)
		img = ImageTk.PhotoImage(image=self.image)
		panel = tk.Label(self, image=img)
		panel.image = img
		panel.pack()


	def login(self, gui, username, password):
		# parameter: gui -> The GUI that is being used.
		# parameter: username -> The username the client provided.
		# parameter: password -> The password the client provided.

		"""
		Checks to see if client entered information for both
		the username and password fields.
		"""
		if (username and password):

			# CODE NEEDED: Encrpty password
			response = gui.getClient().login(username, password)

			"""
			Checks to see if the there is any problems with loginning.
			"""
			if (response == -1):
				tkinter.messagebox.showinfo("Warning", "Server failed to respond!")

				"""
				Empties the textboxes to reenter information.
				"""
				self.usernameInput.delete(0, 'end')
				self.passwordInput.delete(0, 'end')
				# Clear these out since certain parameters are persistent objects?
				username = ""
				password = ""
			elif (response == 0):
				tkinter.messagebox.showinfo("Warning", "Invalid login information.")

				"""
				Empties the textboxes to reenter information.
				"""
				self.usernameInput.delete(0, 'end')
				self.passwordInput.delete(0, 'end')
				# Clear these out since certain parameters are persistent objects?
				username = ""
				password = ""
			else:
				"""
				Empties the textboxes.
				"""
				print("Login Successfully")
				self.usernameInput.delete(0, 'end')
				self.passwordInput.delete(0, 'end')
				# Clear these out since certain parameters are persistent objects?
				username = ""
				password = ""
				gui.show_frame(menu.MenuPage)

		# Checks to see if client didn't enter a password.
		elif username:
			tkinter.messagebox.showinfo("Warning", "Please enter a password.")

		# Checks to see if client didn't enter a username.
		elif (password):
			tkinter.messagebox.showinfo("Warning", "Please enter a username.")

		# Checks to see if client didn't any login information.
		else:
			tkinter.messagebox.showinfo("Warning", "Please enter a username and password.")

	def back(self, gui):
		# parameter: gui -> The GUI that is being used.

		"""
		Empties the textboxes before heading back to the starting page.
		"""
		self.usernameInput.delete(0, 'end')
		self.passwordInput.delete(0, 'end')

		"""
		Goes back to starting page.
		"""
		gui.show_frame(start.StartPage)
