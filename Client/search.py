import tkinter as tk

from tkinter import TOP, E

from Client import menu


class SearchPage(tk.Frame):
	def __init__(self, frame, gui):
		tk.Frame.__init__(self, frame)

		label = tk.Label(self, text = "Search")
		label.pack(side=TOP)

		#Frame used for organization
		top = tk.Frame(self)
		top.pack(side=TOP)

		#Frame used for organization
		bottom = tk.Frame(self)
		bottom.pack(side=TOP)

		searchText = tk.Label(top, text = "Search")
		searchText.grid(row=0, sticky=E)

		self.searchInput = tk.Entry(top)
		self.searchInput.grid(row=0, column=1)

		searchButton = tk.Button(bottom, text="Search",
								command = lambda: self.search(gui, self.searchInput.get()))
		searchButton.grid(row=0)

		backButton = tk.Button(bottom, text="Back",
							command = lambda: self.back(gui))
		backButton.grid(row=0, column=1)

	def search(self, gui, filename):
		response = gui.getClient().search(filename)
		self.searchInput.delete(0, 'end')

	def back(self, gui):
		#parameter: gui -> The GUI that is being used.

		"""
		Empties the textbox before heading back to the starting page.
		"""
		self.searchInput.delete(0, 'end')

		"""
		Goes back to the starting page.
		"""
		gui.show_frame(menu.MenuPage)