import tkinter as tk

from tkinter import filedialog
from tkinter import *
from tkinter import TOP, E
import tkinter.messagebox

from Client import menu, repoids, global_username, SHARED_REPO_ID


class UploadPage(tk.Frame):
    def __init__(self, frame, gui):
        # parameter: frame
        # parameter: gui

        """
        Init the frame.
        """
        tk.Frame.__init__(self, frame)

        self.client = gui.getClient()

        """
        Creates a Label to display 'Upload'.
        """
        label = tk.Label(self, text="Upload")
        label.pack(side=TOP)

        # Frame used for organization
        top = tk.Frame(self)
        self.top = top
        top.pack(side=TOP)

        groupInfoFrame = tk.Frame(self)
        groupInfoFrame.pack()

        # Frame used for organization
        bottom = tk.Frame(self)
        bottom.pack(side=TOP)

        """
        Creates a Label to display 'Filename'.
        """
        filenameText = tk.Label(top, text="Filename")
        filenameText.grid(row=0, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the name of the file.
        """
        self.filenameInput = tk.Entry(top)
        self.filenameInput.grid(row=0, column=1)

        self.file_path = None

        """
        Creates and adds a back button.
        Takes the client back to menu page when clicked on.
        """
        searchButton = tk.Button(top, text="Search",
                                 command=lambda: self.searchClientFile(gui))
        searchButton.grid(row=0, column=2)

        """
        Creates a Label to display 'Tags'.
        """
        tagsText = tk.Label(top, text="Tags")
        tagsText.grid(row=1, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the category of the file.
        """
        self.tagsInput = tk.Entry(top)
        self.tagsInput.grid(row=1, column=1)

        """
        Creates a Label to display 'Comments'.
        """
        commentsText = tk.Label(top, text="Comments")
        commentsText.grid(row=2, sticky=E)

        """
        Creates a Entry to display a textbox for the client to enter the keywords of the file.
        """
        self.commentsInput = tk.Text(top, width=25, height=3, bd=5)
        self.commentsInput.grid(row=2, column=1)

        repoText = tk.Label(top, text="Repositary")
        repoText.grid(row=3, column=0)

        self.groupNameText = tk.Label(top, text="Group Name")
        self.groupNameInput = tk.Entry(top)

        repoOptionsFrame = tk.Frame(top)
        repoOptionsFrame.grid(row=3, column=1, columnspan=1)

        self.var = StringVar()

        self.repo_destination = StringVar()
        self.repo_destination.set("self")

        selfRB = Radiobutton(repoOptionsFrame, text="Self", variable=self.repo_destination, value="self",
                             command=lambda: self.remove_groupOptions())
        groupRB = Radiobutton(repoOptionsFrame, text="Group", variable=self.repo_destination, value="group",
                              command=lambda: self.show_groupOptions())
        sharedRB = Radiobutton(repoOptionsFrame, text="Shared", variable=self.repo_destination, value="shared",
                               command=lambda: self.remove_groupOptions())

        selfRB.grid(row=0, column=0, sticky=W)
        groupRB.grid(row=0, column=1)
        sharedRB.grid(row=0, column=2)

        """
        Creates and adds a upload button.
        Takes all text the client enters and
        uploads the file with the corresponding information.
        """
        uploadButton = tk.Button(bottom, text="Upload",
                                 command=lambda: self.upload(gui,
                                                             self.filenameInput.get(),
                                                             self.tagsInput.get(),
                                                             self.commentsInput.get("1.0", END)))
        uploadButton.grid(row=0)

        """
        Creates and adds a back button.
        Takes the client back to menu page when clicked on.
        """
        backButton = tk.Button(bottom, text="Back",
                               command=lambda: self.back(gui))
        backButton.grid(row=0, column=1)

    def show_groupOptions(self):
        self.groupNameText.grid(row=4, column=0)
        self.group_names.grid(row=4, column=1)

    def remove_groupOptions(self):
        self.groupNameText.grid_forget()
        self.group_names.grid_forget()

    def get_repo_id(self):
        repo = self.repo_destination.get()
        if repo == "self":
            return repoids[0]
        elif repo == "group":
            for group_tuple in self.list_groups:
                if group_tuple[1] == self.var.get():
                    return group_tuple[0]
        elif repo == "shared":
            return SHARED_REPO_ID

    def upload(self, gui, filename, tag, comment):
        if not filename and not tag and len(comment) == 1:
            tkinter.messagebox.showinfo("Warning", "Please enter the name of a file, a tag, and a comment.")

        elif not filename:
            tkinter.messagebox.showinfo("Warning", "Please enter the name of a file or search for one on your machine.")

        elif not tag:
            tkinter.messagebox.showinfo("Warning", "Please enter a tag.")

        elif len(comment) == 1:
            tkinter.messagebox.showinfo("Warning", "Please enter a comment.")

        elif filename and tag and comment:
            repo_id = self.get_repo_id()
            if self.file_path:
                response = gui.getClient().upload(self.file_path, [tag], comment, str(repo_id))
            else:
                response = gui.getClient().upload(filename, [tag], comment, str(repo_id))

            if not response:
                tkinter.messagebox.showinfo("Warning", "File " + filename + " was not found. The file was not uploaded")

            elif response:
                tkinter.messagebox.showinfo("Notice", "File " + filename + " was sucessfully uploaded.")

            self.filenameInput.delete(0, 'end')
            self.tagsInput.delete(0, 'end')
            self.commentsInput.delete("1.0", END)
            self.file_path = None

    def searchClientFile(self, gui):
        gui.filename = filedialog.askopenfilename(initialdir="/", title="Select file")

        print(gui.filename)

        path = gui.filename.split("/")
        print(path[-1])
        filename = path[-1]
        self.filenameInput.delete(0, 'end')
        self.filenameInput.insert(0, filename)

        self.file_path = gui.filename

    def back(self, gui):
        # parameter: gui -> The GUI that is being used.

        """
        Empties the textboxes before heading back to the starting page.
        """
        self.filenameInput.delete(0, 'end')
        self.tagsInput.delete(0, 'end')
        self.commentsInput.delete("1.0", END)
        self.repo_destination.set("self")
        try:  # god forgive my sins
            self.group_names.destroy()
        except AttributeError:
            pass  # ignore if group_names does not exist

        """
        Goes back to the starting page.
        """
        gui.show_frame(menu.MenuPage)

    def on_show(self):
        self.list_groups = self.client.retrieve_groups(global_username[0])
        if self.list_groups:
            self.var.set(self.list_groups[0][1])
        else:
            self.var.set(" ")
        print(self.list_groups)

        self.group_names = tk.OptionMenu(self.top, self.var, *[tup[1] for tup in self.list_groups]
                                                                if self.list_groups else " ")

