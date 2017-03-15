__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

import tkinter as tk

from tkinter import filedialog
from tkinter import *
from tkinter import TOP, E

from Server import home_gui


class SettingsPage(tk.Frame):
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
        label = tk.Label(self, text="Server Settings")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=BOTTOM)

        # http://effbot.org/tkinterbook/radiobutton.htm
        certModeText = tk.Label(top, text="SSL Certificate Mode")
        certModeText.grid(row=0, sticky=N)

        certModes = [
            ("Automatic Let's Encrypt Certificate", 1),
            ("Manually Selected Certificate:", 2),
            ("Self-Signed Certificate (WARNING: INSECURE)", 3)
        ]
        gui.selectedCertMode = IntVar()
        gui.selectedCertMode.set(1)
        for title, val in certModes:
            Radiobutton(self,
                        text=title,
                        padx=10,
                        variable=gui.selectedCertMode,
                        command=lambda: self.certModeChanged(gui),
                        value=val).pack(side=TOP, anchor=W)

        ''''
        """
        Creates a Label to display 'Certificate File'.
        """
        filenameText = tk.Label(top, text="Certificate File")
        filenameText.grid(row=2, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the name of the file.
        """
        self.filenameInput = tk.Entry(top)
        self.filenameInput.grid(row=2, column=1)

        """
        Creates a Label to display 'Private Key File'.
        """
        categoryText = tk.Label(top, text="Private Key File")
        categoryText.grid(row=3, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the category of the file.
        """
        self.categoryInput = tk.Entry(top)
        self.categoryInput.grid(row=3, column=1)

        """
                Creates and adds a select private key file button.
                Opens a file-browser window which only accepts a .key file.
        """
        uploadButton = tk.Button(bottom, text="Upload",
                                 command=lambda: self.upload(gui,
                                                             self.filenameInput.get(),
                                                             self.categoryInput.get(),
                                                             self.keywordsInput.get()))
        uploadButton.grid(row=0)

        """
        Creates a Label to display 'Certificate Server Hostname'.
        """
        keywordsText = tk.Label(top, text="Certificate Server Hostname")
        keywordsText.grid(row=4, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the keywords of the file.
        """
        self.keywordsInput = tk.Entry(top)
        self.keywordsInput.grid(row=4, column=1)

        """
        Creates and adds a upload button.
        Takes all text the client enters and
        uploads the file with the corresponding information.
        """
        uploadButton = tk.Button(bottom, text="Upload",
                                 command=lambda: self.manually_set_keyfile(gui))
        uploadButton.grid(row=0)'''

        """
        Creates and adds a back button.
        Takes the client back to menu page when clicked on.
        """
        backButton = tk.Button(bottom, text="Cancel",
                               command=lambda: self.back(gui))
        backButton.grid(row=2)


    def certModeChanged(self, gui):
        # Add code in here which enables and distables certain fields
        # based upon the selection.
        gui.selectedCertMode
        if (gui.selectedCertMode.get() == 3):
            # Put in fields for Self Signed Certificate
            print("IMPLEMENT CERT SETTINGS FOR SELF SIGNED CERTS")
        elif (gui.selectedCertMode.get() == 2):
            # Put in fields for Manually Selected Certificate
            print("IMPLEMENT CERT SETTINGS FOR MANUAL FIELDS")
        elif (gui.selectedCertMode.get() == 1):
            # Put in fields for Automatic Let's Encrypt Certificate
            print("IMPLEMENT CERT SETTINGS FOR AUTOMATIC FIELDS")



    def manually_set_certfile(self, gui):
        # Open a file window which allows you to select only a '.crt' file and bind the value to the main gui object
        gui.certFilename = filedialog.askopenfilename(initialdir="/", title="Select Certificate File",
                                                      filetypes=[('Certificate', '.crt')])

    def manually_set_keyfile(self, gui):
        # Open a file window which allows you to select only a '.key' file and bind the value to the main gui object
        gui.keyFilename = filedialog.askopenfilename(initialdir="/", title="Select Private Key File",
                                                      filetypes=[('Private Key', '.key')])

    def apply_settings(self, gui, filename, category, keywords):
        # TODO: Change to use the above methods for setting the keyfiles.
        # TODO: Also needs to evenually allow for LE certs and self-signed.

        gui.keyFilename = filedialog.askopenfilename(initialdir="/", title="Select file")
        print(gui.filename)
        self.filenameInput.insert(0, gui.filename)
        response = gui.getClient().upload(filename, category, keywords)
        """
            Goes back to the home page.
        """
        gui.show_frame(home_gui.HomePage)

    # self.filenameInput.delete(0, 'end')
    # self.categoryInput.delete(0, 'end')
    # self.keywordsInput.delete(0, 'end')

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Goes back to the starting page.
        """
        gui.show_frame(home_gui.HomePage)
