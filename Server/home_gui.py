__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

import os
import tkinter as tk
from tkinter import LEFT, BOTTOM

from Server import gui
from Server import settings_gui
from Server import server


class HomePage(tk.Frame):
	def __init__(self, frame, gui):
		#parameter: frame -> The frame that will be initialied.
		#parameter: gui -> The GUI object that is being used.

		"""
		Initializes the frame that was passed in.
		"""
		tk.Frame.__init__(self, frame)

		#Frame used for organization
		bottom = tk.Frame(self)
		bottom.pack(side=BOTTOM)

		"""
		Creates a label to display window name on the screen.
		"""
		label = tk.Label(self, text="KM Server Management")
		label.pack()

		"""
		Creates and adds the login button.
		Takes the client to the login page when clicked on.
		"""
		startButton = tk.Button(bottom, text = "Start Server",
							command = lambda: self.server_start_commands(gui))
		startButton.pack(side = LEFT)

		"""
		Creates and adds the register button.
		Takes the client to the register page when clicked on.
		"""
		stopButton = tk.Button(bottom, text = "Stop Server",
							command = lambda: self.server_shutdown_commands(gui))
		stopButton.pack(side = LEFT)

		"""
			Creates and adds the register button.
			Takes the client to the register page when clicked on.
		"""
		settingsButton = tk.Button(bottom, text="Server Settings",
							   command=lambda: gui.show_frame(settings_gui.SettingsPage))
		settingsButton.pack(side=LEFT)

		"""
		Creates and adds the exit button.
		Closes the window and exits the program when clicked on.
		"""
		exitButton = tk.Button(bottom, text = "Exit", command = lambda: self.server_quit_commands(gui))
		exitButton.configure(command=self.quit)
		exitButton.pack(side = LEFT)

	def server_shutdown_commands(self, gui):
		gui.getServer().server_shutdown()
		gui.getServer().stop()
		gui.setServer(None)

	def server_start_commands(self, gui):
		gui.setServer(server.Server(gui))
		gui.getServer().start()

	def server_quit_commands(self, gui):
		if gui.getServer() != None:
			self.server_shutdown_commands(gui)
		#self.quit