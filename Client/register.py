import tkinter as tk

from tkinter import TOP, E
import tkinter.messagebox

from Client import gui
from Client import start
from Client import menu

import re


class RegisterPage(tk.Frame):
    def __init__(self, frame, gui):
        # parameter: frame -> The frame that will be initialized.
        # parameter: gui -> The GUI object that is being used.

        """
        Initializes the frame that was passed in.
        """
        tk.Frame.__init__(self, frame)

        """
        Creates a label to display window name.
        """
        label = tk.Label(self, text="Register")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=TOP)

        """
        Creates a Label to display 'Create a Username'
        """
        self.usernameText = tk.Label(top, text="Create a Username:")
        self.usernameText.grid(row=1, column=0, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter their username.
        """
        self.usernameInput = tk.Entry(top)
        self.usernameInput.grid(row=1, column=1, sticky=E)

        """
        Creates a Label to display 'Create a Password'
        """
        self.passwordText = tk.Label(top, text="Create a Password:")
        self.passwordText.grid(row=2, column=0, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter their password.
        The text is hidden using '•'.
        """
        self.passwordInput = tk.Entry(top, show='•')
        self.passwordInput.grid(row=2, column=1, sticky=E)

        """
        Creates a Label to display 'Create a Password'
        """
        self.sec_questionText = tk.Label(top, text="Security Question:")
        self.sec_questionText.grid(row=3, column=0, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter their password.
        """
        self.sec_questionInput = tk.Entry(top)
        self.sec_questionInput.grid(row=3, column=1, sticky=E)

        """
        Creates a Label to display 'Create a Password'
        """
        self.sec_answerText = tk.Label(top, text="Security Answer:")
        self.sec_answerText.grid(row=4, column=0, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter their password.
        """
        self.sec_answerInput = tk.Entry(top)
        self.sec_answerInput.grid(row=4, column=1, sticky=E)

        """
        Creates and adds the sign up button.
        Creates a new user account and takes the client to the menu page when clicked on.
        """
        signUpButton = tk.Button(bottom, text="Sign-Up",
                                 command=lambda: self.register(gui, self.usernameInput.get(), self.passwordInput.get(),
                                                               self.sec_questionInput.get(), self.sec_answerInput.get()))
        signUpButton.grid(row=0)

        """
        Creates and adds the back button.
        Takes the client back to the starting page when clicked.
        """
        backButton = tk.Button(bottom, text="Back", command=lambda: self.back(gui))
        backButton.grid(row=0, column=1)

    def register(self, gui, username, password, sec_question, sec_answer):
        if (username and password):
            if (len(password) < 8):
                """
                Displays a pop up if username is not available.
                Clears both textboxes to enter new information.
                """
                tkinter.messagebox.showinfo("Warning", "Password must be at least 12 characters long!")
                self.usernameInput.delete(0, 'end')
                self.passwordInput.delete(0, 'end')
                self.sec_answerInput.delete(0, 'end')
                self.sec_questionInput.delete(0, 'end')
                # Clear these out since certain parameters are persistent objects?
                username = ""
                password = ""
            elif (re.search(r"\d", password) is None):
                """
                Displays a pop up if username is not available.
                Clears both textboxes to enter new information.
                """
                tkinter.messagebox.showinfo("Warning", "Password must contain a number!")
                self.usernameInput.delete(0, 'end')
                self.passwordInput.delete(0, 'end')
                self.sec_answerInput.delete(0, 'end')
                self.sec_questionInput.delete(0, 'end')
                # Clear these out since certain parameters are persistent objects?
                username = ""
                password = ""
            elif (re.search(r"[A-Z]", password) is None):
                """
                Displays a pop up if username is not available.
                Clears both textboxes to enter new information.
                """
                tkinter.messagebox.showinfo("Warning", "Password must contain an uppercase letter!")
                self.usernameInput.delete(0, 'end')
                self.passwordInput.delete(0, 'end')
                self.sec_answerInput.delete(0, 'end')
                self.sec_questionInput.delete(0, 'end')
                # Clear these out since certain parameters are persistent objects?
                username = ""
                password = ""
            elif (re.search(r"[a-z]", password) is None):
                """
                Displays a pop up if username is not available.
                Clears both textboxes to enter new information.
                """
                tkinter.messagebox.showinfo("Warning", "Password must contain a lowercase letter!")
                self.usernameInput.delete(0, 'end')
                self.passwordInput.delete(0, 'end')
                self.sec_answerInput.delete(0, 'end')
                self.sec_questionInput.delete(0, 'end')
                # Clear these out since certain parameters are persistent objects?
                username = ""
                password = ""
            elif (re.search(r"[!#$%&'()*+,-./]", password) is None):
                """
                Displays a pop up if username is not available.
                Clears both textboxes to enter new information.
                """
                tkinter.messagebox.showinfo("Warning", "Password must contain a special character!")
                self.usernameInput.delete(0, 'end')
                self.passwordInput.delete(0, 'end')
                self.sec_answerInput.delete(0, 'end')
                self.sec_questionInput.delete(0, 'end')
                # Clear these out since certain parameters are persistent objects?
                username = ""
                password = ""
            else:
                # CODE NEEDED: Encrypt Password
                response = gui.getClient().register(username, password, sec_question, sec_answer)

                """
                Checks to see if username is available.
                """
                if (response == False):
                    """
                    Displays a pop up if username is not available.
                    Clears both textboxes to enter new information.
                    """
                    tkinter.messagebox.showinfo("Warning",
                                                "Account already exist with that username. Please enter another one.")
                    self.usernameInput.delete(0, 'end')
                    self.passwordInput.delete(0, 'end')
                    # Clear these out since certain parameters are persistent objects?
                    username = ""
                    password = ""
                else:
                    """
                    Creates a new account.
                    Clears both textboxes.
                    Takes the user to the menu page.
                    """
                    print("Account created")
                    self.usernameInput.delete(0, 'end')
                    self.passwordInput.delete(0, 'end')
                    # Clear these out since certain parameters are persistent objects?
                    username = ""
                    password = ""
                    gui.show_frame(menu.MenuPage)

                    # Checks to see if client didn't enter a password.
        elif (username):
            tkinter.messagebox.showinfo("Warning", "Please enter a password.")

            # Checks to see if client didn't enter a username.
        elif (password):
            tkinter.messagebox.showinfo("Warning", "Please enter a username.")

            # Checks to see if client didn't enter any information.
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
        Goes back to the starting page.
        """
        gui.show_frame(start.StartPage)
