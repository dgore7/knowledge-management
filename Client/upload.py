import tkinter as tk

from tkinter import filedialog
from tkinter import *
from tkinter import TOP, E

import menu


class UploadPage(tk.Frame):
    def __init__(self, frame, gui):
        # parameter: frame
        # parameter: gui

        """
        Init the frame.
        """
        tk.Frame.__init__(self, frame)

        """
        Creates a Label to display 'Upload'.
        """
        label = tk.Label(self, text="Upload")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=TOP)

        """
        Creates a Label to display 'Filename'.
        """
        filenameText = tk.Label(top, text="Filename")
        filenameText.grid(row=0, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the name of the file.
        """
        self.filenameInput = tk.Entry(top)
        self.filenameInput.grid(row=0, column=1)

        """
        Creates a Label to display 'Category'.
        """
        categoryText = tk.Label(top, text="Category")
        categoryText.grid(row=1, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the category of the file.
        """
        self.categoryInput = tk.Entry(top)
        self.categoryInput.grid(row=1, column=1)

        """
        Creates a Label to display 'Keywords'.
        """
        keywordsText = tk.Label(top, text="Keywords")
        keywordsText.grid(row=2, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the keywords of the file.
        """
        self.keywordsInput = tk.Entry(top)
        self.keywordsInput.grid(row=2, column=1)

        """
        Creates and adds a upload button.
        Takes all text the client enters and
        uploads the file with the corresponding information.
        """
        uploadButton = tk.Button(bottom, text="Upload",
                                 command=lambda: self.upload(gui,
                                                             self.filenameInput.get(),
                                                             self.categoryInput.get(),
                                                             self.keywordsInput.get()))
        uploadButton.grid(row=0)

        """
        Creates and adds a back button.
        Takes the client back to menu page when clicked on.
        """
        backButton = tk.Button(bottom, text="Back",
                               command=lambda: self.back(gui))
        backButton.grid(row=0, column=1)

    def upload(self, gui, filename, category, keywords):
        gui.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        print(gui.filename)
        self.filenameInput.insert(0, gui.filename)
        response = gui.getClient().upload(filename, category, keywords)

    # self.filenameInput.delete(0, 'end')
    # self.categoryInput.delete(0, 'end')
    # self.keywordsInput.delete(0, 'end')

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Empties the textboxes before heading back to the starting page.
        """
        self.filenameInput.delete(0, 'end')
        self.categoryInput.delete(0, 'end')
        self.keywordsInput.delete(0, 'end')

        """
        Goes back to the starting page.
        """
        gui.show_frame(menu.MenuPage)
