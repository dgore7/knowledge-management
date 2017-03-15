__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"



import tkinter as tk

from tkinter import TOP, E

from Client import menu


class RetrievePage(tk.Frame):
    def __init__(self, frame, gui):
        tk.Frame.__init__(self, frame)

        label = tk.Label(self, text="Retrieve")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=TOP)

        retrieveText = tk.Label(top, text="Filename")
        retrieveText.grid(row=0, sticky=E)

        self.retrieveInput = tk.Entry(top)
        self.retrieveInput.grid(row=0, column=1)

        retrieveButton = tk.Button(bottom, text="Retrieve",
                                   command=lambda: self.retrieve(gui, self.retrieveInput.get()))
        retrieveButton.grid(row=0)

        backButton = tk.Button(bottom, text="Back",
                               command=lambda: self.back(gui))
        backButton.grid(row=0, column=1)

    def retrieve(self, gui, filename):
        response = gui.getClient().retrieve(filename)
        self.retrieveInput.delete(0, 'end')

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Empties the textbox before heading back to the starting page.
        """
        self.retrieveInput.delete(0, 'end')

        """
        Goes back to the starting page.
        """
        gui.show_frame(menu.MenuPage)
