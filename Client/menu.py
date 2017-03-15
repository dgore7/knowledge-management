__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

import tkinter as tk

from tkinter import *
from PIL import ImageTk, Image


from Client import start
from Client import upload
from Client import search
from Client import group
from Client import group_management


class MenuPage(tk.Frame):
    def __init__(self, frame, gui):
        tk.Frame.__init__(self, frame)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=TOP)

        label = tk.Label(top, text="Main Menu")
        label.pack()

        # Frame used for organization
        left = tk.Frame(bottom, bd=25, relief=RAISED)
        left.grid(row=0)

        # Frame used for organization
        right = tk.Frame(bottom, bd=25, relief=RAISED)
        right.grid(row=0, column=1)

        """
        Creates and adds the upload button.
        Takes the client to the upload page when clicked.
        """
        uploadButton = tk.Button(left, text="Upload File",
                                 command=lambda: gui.show_frame(upload.UploadPage))
        uploadButton.pack()
        """
        Creates and adds the retrieve button.
        Takes the client to the retrieve page when clicked.
        """
        # retrieveButton = tk.Button(left, text = "Retrive File",
        # 						 command = lambda: gui.show_frame(retrieve.RetrievePage))
        # retrieveButton.pack()

        """
        Creates and adds the search button.
        Takes the client to the search page when clicked.
        """
        searchButton = tk.Button(left, text="Search File",
                                 command=lambda: gui.show_frame(search.SearchPage))
        searchButton.pack()

        createGroupsButton = tk.Button(left, text="Create Groups",
                                       command=lambda: gui.show_frame(group.GroupPage))
        createGroupsButton.pack()

        """
        Creates and adds the delete button.
        Takes the client to the delete page when clicked.
        """
        # deleteButton = tk.Button(right, text = "Delete File",
        # 						 command = lambda: gui.show_frame(delete.DeletePage))
        # deleteButton.pack()
        groupManagementButton = tk.Button(right, text="Group Management",
                                          command=lambda: gui.show_frame(group_management.GroupManagementPage))
        groupManagementButton.pack()

        """
        Creates and adds the quit button.
        Closes the window and stops the program.
        """
        quitButton = tk.Button(right, text="Quit", command=self.quit)
        quitButton.pack(ipadx=18)

        """
        Creates and adds the logout button.
        Takes the client back to the starting page when clicked.
        """
        logoutButton = tk.Button(right, text="Log Out",
                                 command=lambda: gui.show_frame(start.StartPage))
        logoutButton.pack(ipadx=6)

        image = Image.open("penguin.png")
        self.image = Image.composite(image, Image.new('RGB', image.size, 'white'), image)
        img = ImageTk.PhotoImage(image=self.image)
        panel = tk.Label(self, image=img)
        panel.image = img
        panel.pack()


    def update_and_search(self, gui):
        gui.show_frame(search.SearchPage)
        print("Hello")
