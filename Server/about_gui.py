__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

import tkinter as tk

from tkinter import filedialog
from tkinter import *
from tkinter import TOP, E

from Server import home_gui


class AboutPage(tk.Frame):
    def __init__(self, frame, gui):
        # parameter: frame
        # parameter: gui

        """
        Init the frame.
        """
        tk.Frame.__init__(self, frame)

        """
        Creates a Label to display 'Server Settings'.
        """
        label = tk.Label(self, text="About Knowledge Management")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=BOTTOM)

        # http://effbot.org/tkinterbook/radiobutton.htm
        programVersionText = tk.Label(top, text="Version 0.9")
        programVersionText.grid(row=0, sticky=N)
        titleContributersText = tk.Label(top, text="Written by: ")
        titleContributersText.grid(row=1, sticky=N)
        contributersText = tk.Label(top, text="Ayadullah Syed, David Gorelik, Jasmine Farley,\n"
                                          "Jessica Hua, Jose Palacios, Josh Smith,\n"
                                          "Serafin Balcazar, and Steve Saucedo")
        contributersText.grid(row=2, sticky=N)

        backButton = tk.Button(bottom, text="Cancel",
                               command=lambda: self.back(gui))
        backButton.grid(row=2)


    def back(self, gui):
        """
        Goes back to the starting page.
        """
        gui.show_frame(home_gui.HomePage)
