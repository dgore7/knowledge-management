import tkinter as tk

from tkinter import RIGHT, END, ACTIVE, StringVar
import tkinter.messagebox


from Client import menu, global_username


class GroupManagementPage(tk.Frame):
    def __init__(self, frame, gui):
        tk.Frame.__init__(self, frame)
        self.var = StringVar()
        self.list_groups = []
        label = tk.Label(self, text="Group Management")
        label.pack()

        self.client = gui.getClient()

        top = tk.Frame(self)
        top.pack()

        memberLabel = tk.Label(top, text="Member Name")
        memberLabel.grid(row=0, column=0)

        self.memberEntry = tk.Entry(top)
        self.memberEntry.grid(row=0, column=1)

        addButton = tk.Button(top, text="Add Member", command=lambda: self.addMember(gui,
                                                                                     self.memberEntry.get()))
        addButton.grid(row=0, column=2)

        middle = tk.Frame(self)
        middle.pack()

        membersLabel = tk.Label(middle, text="Group Members")
        membersLabel.pack()

        self.list_members = tk.Listbox(middle)
        self.list_members.pack()

        removeButton = tk.Button(middle, text="Remove", command=lambda: self.removeMember(gui))
        removeButton.pack(side=RIGHT)

        bottom = tk.Frame(self)
        bottom.pack()

        backButton = tk.Button(bottom, text="Back", command=lambda: self.back(gui))
        backButton.pack()

    def addMember(self, gui, member_name):
        print(self.var.get())
        if member_name == "":
            tkinter.messagebox.showinfo("Warning", "Please enter the name of a member to add.")

        elif member_name in self.list_members.get(0, END):
            tkinter.messagebox.showinfo("Warning", member_name + " is already in the list.")

        else:
            result = tkinter.messagebox.askyesno("Add Member", "Do you want to add " + member_name + " to the group?")
            if result:
                response = gui.getClient().addMember(member_name)

                if response == "SUCCESS":
                    tkinter.messagebox.showinfo("Notice", "Successfully added " + member_name)

                self.list_members.insert(END, member_name)
            self.memberEntry.delete(0, 'end')

    def removeMember(self, gui):
        print(self.var.get())
        member_name = self.list_members.get(ACTIVE)

        if member_name:
            result = tkinter.messagebox.askyesno("Remove Member",
                                                 "Do you want to remove " + member_name + " from the group?")
            if result:
                response = gui.getClient().removeMember(member_name)
                if response == "SUCCESS":
                    tkinter.messagebox.showinfo("Notice", "Successfully removed " + member_name)
                    self.list_members.delete(ACTIVE)

    def back(self, gui):
        self.memberEntry.delete(0, 'end')
        self.list_members.delete(0, END)
        self.group_names.destroy()

        gui.show_frame(menu.MenuPage)

    def on_show(self):
        self.list_groups = self.client.retrieve_groups(global_username[0])
        if self.list_groups:
            self.var.set(self.list_groups[0][1])
        else:
            self.var.set(" ")
        print(self.list_groups)

        self.group_names = tk.OptionMenu(self, self.var, *[tup[1] for tup in self.list_groups]
                                                                if self.list_groups else " ")
        self.group_names.pack()
