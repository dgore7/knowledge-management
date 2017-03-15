__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

import tkinter as tk
from tkinter import LEFT, BOTTOM

from Client import login
from Client import register


class StartPage(tk.Frame):
    def __init__(self, frame, gui):
        # parameter: frame -> The frame that will be initialied.
        # parameter: gui -> The GUI object that is being used.

        """
        Initializes the frame that was passed in.
        """
        tk.Frame.__init__(self, frame)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=BOTTOM)

        """
        Creates a label to display window name on the screen.
        """
        label = tk.Label(self, text="Start Page")
        label.pack()

        """
        Creates and adds the login button.
        Takes the client to the login page when clicked on.
        """
        loginButton = tk.Button(bottom, text="Login",
                                command=lambda: gui.show_frame(login.LoginPage))
        loginButton.pack(side=LEFT)

        """
        Creates and adds the register button.
        Takes the client to the register page when clicked on.
        """
        registerButton = tk.Button(bottom, text="Register",
                                   command=lambda: gui.show_frame(register.RegisterPage))
        registerButton.pack(side=LEFT)

        """
        Creates and adds the exit button.
        Closes the window and exits the program when clicked on.
        """
        exitButton = tk.Button(bottom, text="Exit", command=self.quit)
        exitButton.pack(side=LEFT)
