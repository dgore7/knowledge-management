__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

import tkinter as tk

from tkinter import TOP, RIGHT, E, END, ACTIVE
import tkinter.messagebox

from Client import menu, global_username


class GroupPage(tk.Frame):
    def __init__(self, frame, gui):
        tk.Frame.__init__(self, frame)

        self.members = []

        label = tk.Label(self, text="Group")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        top.pack(side=TOP)

        middle = tk.Frame(self)
        middle.pack(side=TOP)

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=TOP)

        groupText = tk.Label(top, text="Create Group")
        groupText.grid(row=0, sticky=E)

        self.groupInput = tk.Entry(top)
        self.groupInput.grid(row=0, column=1)

        member_label = tk.Label(top, text="Member Name")
        member_label.grid(row=1, column=0)

        self.member_entry = tk.Entry(top)
        self.member_entry.grid(row=1, column=1)

        addMember = tk.Button(top, text="Add Member", command=lambda: self.addMember())
        addMember.grid(row=1, column=2)

        membersText = tk.Label(middle, text="Members Adding")
        membersText.pack()

        self.list_members = tk.Listbox(middle)
        self.list_members.pack()

        removeButton = tk.Button(middle, text="Remove", command=lambda: self.removeMember())
        removeButton.pack(side=RIGHT)

        groupButton = tk.Button(bottom, text="Create Group",
                                command=lambda: self.createGroup(gui, self.groupInput.get()))
        groupButton.grid(row=0, column=1)

        backButton = tk.Button(bottom, text="Back",
                               command=lambda: self.back(gui))
        backButton.grid(row=0, column=2)

    def addMember(self):
        member_name = self.member_entry.get()
        if member_name == "":
            tkinter.messagebox.showinfo("Warning", "Please enter the name of a member to add.")

        elif member_name in self.members:
            tkinter.messagebox.showinfo("Warning", member_name + " is already in the list.")

        else:
            self.members.append(member_name)
            print("Adding: " + member_name)
            self.list_members.insert(END, member_name)
            self.member_entry.delete(0, 'end')

    def removeMember(self):
        member_name = self.list_members.get(ACTIVE)

        if member_name:
            result = tkinter.messagebox.askyesno("Remove Member",
                                                 "Do you want to remove " + member_name + " from the list?")
            if result:
                self.members.remove(member_name)
                self.list_members.delete(ACTIVE)

    def createGroup(self, gui, group_name):
        if not group_name and len(self.members) == 0 and self.member_entry.get() == "":
            tkinter.messagebox.showinfo("Warning", "Please enter a for the group and the name of a member.")

        elif len(self.members) == 0 and self.member_entry.get() == "":
            tkinter.messagebox.showinfo("Warning", "Please enter the name of at least one group member.")

        elif not group_name:
            tkinter.messagebox.showinfo("Warning", "Please enter a name for the group.")

        elif group_name:
            if self.member_entry.get():
                self.members.append(self.member_entry.get())
            self.members.append(global_username[0])
            response = gui.getClient().createGroup(group_name, self.members)

            if response > 0:
                tk.messagebox.showinfo("Notice", "Successfully create group: " + group_name)

            self.members = [global_username[0]]
            self.list_members.delete(0, END)
            self.groupInput.delete(0, 'end')
            self.member_entry.delete(0, 'end')

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Empties the textbox before heading back to the starting page.
        """

        self.members = []
        self.list_members.delete(0, END)
        self.groupInput.delete(0, 'end')
        self.member_entry.delete(0, 'end')

        """
        Goes back to the starting page.
        """
        gui.show_frame(menu.MenuPage)
