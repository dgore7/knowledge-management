import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

from tkinter import TOP, E

from Client import menu


class SearchPage(tk.Frame):
    def __init__(self, frame, gui):
        tk.Frame.__init__(self, frame)

        self.filename = None

        label = tk.Label(self, text="Search")
        label.pack(side=TOP)

        #####################################################################
        #####################################################################
        #####################################################################

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        searchText = tk.Label(top, text="Search")
        searchText.grid(row=0, column=0, sticky=E)

        self.searchInput = tk.Entry(top)
        self.searchInput.grid(row=0, column=1, sticky=E)

        searchButton = tk.Button(top, text="Search",
                                 command=lambda: self.search(gui, self.searchInput.get()))
        searchButton.grid(row=0, column=2, sticky=E)

        getUpdatesButton = tk.Button(top, text="Get Updates", command=lambda: self.getUpdates())
        getUpdatesButton.grid(row=0, column=3)

        filterButton = tk.Button(top, text="Filter",
                                 command=lambda: self.filter())
        filterButton.grid(row=1)

        self.clicked = 0

        self.monthText = tk.Label(top, text="Month")
        self.monthEntry = tk.Entry(top)

        self.keywordsText = tk.Label(top, text="Keywords")
        self.keywordsEntry = tk.Entry(top)

        self.updateButton = tk.Button(top, text="Update",
                                      command=lambda: self.updateSearch())

        #####################################################################
        #####################################################################
        #####################################################################

        middle = tk.Frame(self)
        middle.pack(side=TOP)

        listFrame = tk.Frame(middle)
        listFrame.grid(row=0, column=0)

        repoLabel = tk.Label(listFrame, text="Repositaries")
        repoLabel.pack()

        selfButton = tk.Button(listFrame, text="Self", command=lambda: self.display_self())
        selfButton.pack(ipadx=14)

        groupButton = tk.Button(listFrame, text="Groups", command=lambda: self.display_groups())
        groupButton.pack()

        sharedButton = tk.Button(listFrame, text="Shared", command=lambda: self.display_shared())
        sharedButton.pack()

        allButton = tk.Button(listFrame, text="All", command=lambda: self.display_all())
        allButton.pack(ipadx=14)

        #####################################################################
        #####################################################################
        #####################################################################

        resultsFrame = tk.Frame(middle)
        resultsFrame.grid(row=0, column=1)

        self.tree = ttk.Treeview(resultsFrame)

        self.tree["columns"] = ("one", "two")
        self.tree.column("#0", width=100)
        self.tree.column("one", width=100)
        self.tree.column("two", width=100)
        self.tree.heading("#0", text="File Name")
        self.tree.heading("one", text="File Size")
        self.tree.heading("two", text="Date")

        self.tree.pack()

        self.tree.bind("<<TreeviewSelect>>", self.OnClick)

        sortingFrame = tk.Frame(middle)
        sortingFrame.grid(row=0, column=2)

        sortingLabel = tk.Label(sortingFrame, text="Sorting Options")
        sortingLabel.pack()

        filenameButton = tk.Button(sortingFrame, text="Filename", command=lambda: self.sortByFilename())
        filenameButton.pack()
        self.filenameButtonClicked = 0

        filesizeButton = tk.Button(sortingFrame, text="Size", command=lambda: self.sortBySize())
        filesizeButton.pack(ipadx=13)
        self.sizeButtonClicked = 0

        filedateButton = tk.Button(sortingFrame, text="Date", command=lambda: self.sortByDate())
        filedateButton.pack(ipadx=11)
        self.updateButtonClicked = 0

        #####################################################################
        #####################################################################
        #####################################################################

        bottom = tk.Frame(self)
        bottom.pack()
        downloadButton = tk.Button(bottom, text="Download", command=lambda: self.download(gui))
        downloadButton.grid(row=0)

        deleteButton = tk.Button(bottom, text="Delete", command=lambda: self.delete(gui))
        deleteButton.grid(row=0, column=1)

        backButton = tk.Button(bottom, text="Back",
                               command=lambda: self.back(gui))
        backButton.grid(row=1, column=1)

    def updateSearch(self):
        if self.monthEntry.get():
            for child in self.tree.get_children():
                if self.monthEntry.get() not in self.tree.item(child, 'values')[1]:
                    self.tree.detach(child)
        if self.keywordsEntry.get():
            print(self.keywordsEntry.get())

        self.monthEntry.delete(0, 'end')
        self.keywordsEntry.delete(0, 'end')

    def filter(self):
        self.clicked += 1
        if self.clicked % 2 == 1:
            self.monthText.grid(row=3, sticky=E)
            self.monthEntry.grid(row=3, column=1)
            self.keywordsText.grid(row=4, sticky=E)
            self.keywordsEntry.grid(row=4, column=1)
            self.updateButton.grid(row=4, column=2)

        else:
            self.monthText.grid_forget()
            self.monthEntry.grid_forget()
            self.keywordsText.grid_forget()
            self.keywordsEntry.grid_forget()
            self.updateButton.grid_forget()

            self.monthEntry.delete(0, 'end')
            self.keywordsEntry.delete(0, 'end')

    def search(self, gui, filename):
        # response = gui.getClient().search(filename)

        self.searchInput.delete(0, 'end')

        for child in self.tree.get_children():
            print(self.tree.item(child, 'text'))
            if filename not in self.tree.item(child, 'text'):
                self.tree.detach(child)
            else:
                print("Found " + filename)

    def sortByFilename(self):
        filenames = []

        currentTree = self.tree.get_children()
        for child in currentTree:
            filenames.append(self.tree.item(child, 'text'))
            self.tree.detach(child)

        self.filenameButtonClicked += 1
        if self.filenameButtonClicked % 2 == 1:
            filenames.sort(reverse=True)
            for filename in filenames:
                for child in currentTree:
                    if self.tree.item(child, 'text') == filename:
                        self.tree.reattach(child, "", 0)
        else:
            filenames.sort()
            for filename in filenames:
                for child in currentTree:
                    if self.tree.item(child, 'text') == filename:
                        self.tree.reattach(child, "", 0)

    def sortBySize(self):
        sizes = []
        currentTree = self.tree.get_children()
        for child in currentTree:
            print(self.tree.item(child, 'values')[0])
            sizes.append(self.tree.item(child, 'values')[0])
            self.tree.detach(child)

        self.sizeButtonClicked += 1
        if self.sizeButtonClicked % 2 == 1:
            sizes.sort(reverse=True)
            for size in sizes:
                for child in currentTree:
                    if self.tree.item(child, 'values')[0] == size:
                        self.tree.reattach(child, "", 0)
        else:
            sizes.sort()
            for size in sizes:
                for child in currentTree:
                    if self.tree.item(child, 'values')[0] == size:
                        self.tree.reattach(child, "", 0)

    def sortByDate(self):
        dates = []
        currentTree = self.tree.get_children()
        for child in currentTree:
            dates.append(self.tree.item(child, 'values')[1])
            self.tree.detach(child)

        self.updateButtonClicked += 1
        if self.updateButtonClicked % 2 == 1:
            dates.sort(reverse=True)
            for date in dates:
                for child in currentTree:
                    if self.tree.item(child, 'values')[1] == date:
                        self.tree.reattach(child, "", 0)

        else:
            dates.sort()
            for date in dates:
                for child in currentTree:
                    if self.tree.item(child, 'values')[1] == date:
                        self.tree.reattach(child, "", 0)

    def display_self(self):
        print(self.tree.get_children())
        print(self.rows)
        for child in self.rows:
            if self.tree.item(child, 'values')[2] != "self":
                self.tree.detach(child)
            else:
                self.tree.reattach(child, "", 0)

    def display_groups(self):
        print(self.rows)
        for child in self.rows:
            if self.tree.item(child, 'values')[2] != "group":
                self.tree.detach(child)
            else:
                self.tree.reattach(child, "", 0)

    def display_shared(self):
        print(self.rows)
        for child in self.rows:
            if self.tree.item(child, 'values')[2] != "shared":
                self.tree.detach(child)
            else:
                self.tree.reattach(child, "", 0)

    def display_all(self):
        for child in self.rows:
            self.tree.reattach(child, "", 0)

    def download(self, gui):
        if self.filename:
            print("Downloading: " + self.filename)
            gui.getClient().download(self.filename)
            self.filename = None
        else:
            print("Error")

    def delete(self, gui):
        if self.filename:
            print("Deleting: " + self.filename)
            result = gui.getClient().delete(self.filename)

            if result == 0:
                tkinter.messagebox.showinfo("Notice", "Successfully deleted: " + self.filename)
                for child in self.tree.get_children():
                    if self.tree.item(child, 'text') == self.filename:
                        self.tree.delete(child)
                self.rows = self.tree.get_children()
            else:
                tkinter.messagebox.showinfo("Warning", "Error occurred: " + self.filename + " was not deleted.")
            self.filename = None
        else:
            print("Error")

    def getUpdates(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

        self.tree.insert("", 0, text="lines.txt", values=("5 bytes", "Feb 25th", "self"))
        self.tree.insert("", 0, text="groups.txt", values=("10 bytes", "Jan 1st", "shared"))
        self.tree.insert("", 0, text="test.txt", values=("7 bytes", "Feb 4th", "group"))
        self.tree.insert("", 0, text="picture.jpg", values=("5 bytes", "Mar 21st", "self"))

        self.rows = self.tree.get_children()

    def OnClick(self, event):
        item = self.tree.selection()[0]
        self.filename = self.tree.item(item, 'text')
        print("Clicked on: " + self.tree.item(item, 'text'))
        print("Additional: " + self.tree.item(item, 'values')[0])

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Empties the textbox before heading back to the starting page.
        """
        self.searchInput.delete(0, 'end')
        self.clicked = 0

        """
        Goes back to the starting page.
        """
        gui.show_frame(menu.MenuPage)
