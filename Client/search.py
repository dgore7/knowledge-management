import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time
from tkinter import *

from tkinter import TOP, E

from Client import menu, PERSONAL, GROUPS, ALL, repoids, global_username, SHARED, SHARED_REPO_ID


class SearchPage(tk.Frame):
    def __init__(self, frame, gui):
        tk.Frame.__init__(self, frame)

        self.filename = None

        self.gui = gui
        self.client = gui.getClient()

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

        # getUpdatesButton = tk.Button(top, text="Get Updates", command=lambda: self.getUpdates())
        # getUpdatesButton.grid(row=0, column=3)

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
        self.list_frame = listFrame

        repoLabel = tk.Label(listFrame, text="Repositories")
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

        self.tree["columns"] = ("owner", "date1", "comment", "number", "date2", "tag")
        self.tree.column("#0", width=100)
        self.tree.column("owner", width=100)
        self.tree.column("date1", width=110)
        self.tree.column("comment", width=100)
        self.tree.column("number", width=100)
        self.tree.column("date2", width=110)
        self.tree.column("tag", width=100)

        self.tree.heading("#0", text="File Name")
        self.tree.heading("owner", text="Owner")
        self.tree.heading("date1", text="Date")
        self.tree.heading("comment", text="Comments")
        self.tree.heading("number", text="Number")
        self.tree.heading("date2", text="Date")
        self.tree.heading("tag", text="Tag")

        self.tree.pack()

        self.tree.bind("<<TreeviewSelect>>", self.OnClick)

        self.group_var = StringVar()
        self.group_var.trace("w", lambda *args: self.getUpdates(GROUPS))
        self.groupNameText = tk.Label(self.list_frame, text="Group Name")

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

        self.comment = StringVar()
        self.commentLabel = tk.Label(self, textvariable=self.comment)
        self.commentLabel.pack()

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

    def show_groupOptions(self):
        self.groupNameText.pack()
        self.group_names.pack()

    def remove_groupOptions(self):
        self.groupNameText.pack_forget()
        self.group_names.pack_forget()

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
        self.remove_groupOptions()
        self.getUpdates(PERSONAL)
        # print(self.tree.get_children())
        # print(self.rows)
        # for child in self.rows:
        #     if self.tree.item(child, 'values')[2] != "self":
        #         self.tree.detach(child)
        #     else:
        #         self.tree.reattach(child, "", 0)

    def display_groups(self):
        self.show_groupOptions()
        self.getUpdates(GROUPS)


    def display_shared(self):
        self.remove_groupOptions()
        self.getUpdates(SHARED)

    def display_all(self):
        self.remove_groupOptions()
        self.getUpdates(ALL)

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

    def display_files(self, files):
        for tup in files:
            date = time.gmtime(float(tup[2]))
            info = str(date[1]) + "/" + str(date[2]) + "/" + str(date[0]) + " " + str(date[3]) + ":" + str(
                date[4]) + ":" + str(date[5])

            another_date = time.gmtime(int(tup[5]))
            more_info = str(another_date[1]) + "/" + str(another_date[2]) + "/" + str(another_date[0]) + " " + str(
                another_date[3]) + ":" + str(another_date[4]) + ":" + str(another_date[5])
            self.tree.insert("", 0, text=tup[0], values=(tup[1], info, tup[3], tup[4], more_info, tup[6]))
        print(files)

    def getUpdates(self, group_type):
        for child in self.tree.get_children():
            self.tree.delete(child)
        result = []
        if group_type is PERSONAL:
            result = self.client.retrieve_repo([repoids[0]])

        elif group_type is GROUPS:
            result = self.client.retrieve_repo([self.get_repo_id()])
        elif group_type is SHARED:
            result = self.client.retrieve_repo([SHARED_REPO_ID])
        elif group_type is ALL:
            result = self.client.retrieve_repo([repoids[0]])
            result.extend(self.client.retrieve_repo([gid for gid in self.group_repo_ids()]))
            result.extend(self.client.retrieve_repo([SHARED_REPO_ID]))
        else:
            # Raise an exception
            pass
        self.display_files(result)

        # for child in self.tree.get_children():
        #     self.tree.delete(child)

        # self.tree.insert("", 0, text="lines.txt", values=("5 bytes", "Feb 25th", "self"))
        # self.tree.insert("", 0, text="groups.txt", values=("10 bytes", "Jan 1st", "shared"))
        # self.tree.insert("", 0, text="test.txt", values=("7 bytes", "Feb 4th", "group"))
        # self.tree.insert("", 0, text="picture.jpg", values=("5 bytes", "Mar 21st", "self"))

        # self.rows = self.tree.get_children()

    def OnClick(self, event):
        item = self.tree.selection()[0]
        self.filename = self.tree.item(item, 'text')
        print("Clicked on: " + self.tree.item(item, 'text'))
        print("Comment: " + self.tree.item(item, 'values')[2])
        self.comment.set("Comment: " + self.tree.item(item, 'values')[2])

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Empties the textbox before heading back to the starting page.
        """
        self.searchInput.delete(0, 'end')
        self.clicked = 0
        self.group_names.pack_forget()

        """
        Goes back to the starting page.
        """
        gui.show_frame(menu.MenuPage)

    def get_repo_id(self):
        repo_name = self.group_var.get()
        for group_tuple in self.list_groups:
            if group_tuple[1] == repo_name:
                return group_tuple[0]

    def group_repo_ids(self):
        for group_tuple in self.list_groups:
            yield group_tuple[0]

    def on_show(self):
        self.list_groups = self.client.retrieve_groups(global_username[0])
        if self.list_groups:
            self.group_var.set(self.list_groups[0][1])
        else:
            self.group_var.set(" ")
        print(self.list_groups)

        self.group_names = tk.OptionMenu(self.list_frame, self.group_var,
                         *[tup[1] for tup in self.list_groups] if self.list_groups else " ")
        for child in self.tree.get_children():
            self.tree.delete(child)
