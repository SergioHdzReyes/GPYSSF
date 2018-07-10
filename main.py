#! /usr/bin/env python
# coding=utf-8
import Tkinter as tk
from Tkinter import Tk
from git import Repo
import os
from Directories import Directories

dir_path = os.path.dirname(os.path.realpath(__file__))
print dir_path

class Application(tk.Frame):
    """Clase principal para correr la interfaz de la sincronizacion de archivos"""

    root_dir = ''
    files_with_changes = []
    error_exception = ''
    dirs = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        try:
            self.repo = Repo()
        except Exception:
            self.set_not_repository_available()
            return

        self.set_repository_information()
        self.createWidgets()

        self.root_dir = dir_path

        self.set_files_with_changes()

        self.dirs = Directories(self.files_with_changes, self.root_dir)
        self.dirs.set_directories_list()

        self.dirs.print_directories_list()

        self.draw_checkbox_files()

    def set_repository_information(self):
        self.repo_info = tk.LabelFrame(self, text="Informacion del repositorio")
        self.repo_info.grid()

        branches = [h.name for h in self.repo.heads]

        text = "\nRama actual: " + str(self.repo.active_branch) + \
               "\nRamas: " + str(branches)

        self.left = tk.Label(self.repo_info, text=text)
        self.left.grid()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text="Cerrar", command=self.quit)
        self.quitButton.grid()

    def set_files_with_changes(self):
        files = os.popen('git status -s | cut -c4-', 'r')
        self.files_with_changes = files.read().strip().split('\n')
        print 'Git status result:'
        print self.files_with_changes

    def draw_checkbox_files(self):
        for file in self.dirs.files_with_changes:
            self.check = tk.Checkbutton(self, text=str(file))
            self.check.grid()

    def set_not_repository_available(self, message='Not repository found'):
        self.repo_info = tk.LabelFrame(self, text=message)
        self.repo_info.grid()

        self.left = tk.Label(self.repo_info, text=message)
        self.left.grid()

        self.quitButton = tk.Button(self, text="Cerrar", command=self.quit)
        self.quitButton.grid()


root = Tk()
app = Application(master=root)
app.master.title('Sincronizar archivos')
app.mainloop()
app.destroy()