#! /usr/bin/env python
# coding=utf-8
import Tkinter as tk
from Tkinter import Tk
from git import Repo
import os
import sys
from os import system
from platform import system as platform
from Directories import Directories

if len(sys.argv) > 1:
    dir_path = sys.argv[1]
    os.chdir(sys.argv[1])
else:
    dir_path = os.path.dirname(os.path.realpath(__file__))


class Application(tk.Frame):
    """Clase principal para correr la interfaz de la sincronizacion de archivos"""

    root_dir = ''
    files_with_changes = []
    error_exception = ''
    dirs = None
    checkboxes = []

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        try:
            self.repo = Repo(dir_path)
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
            self.checkboxes.append(tk.Checkbutton(self, text=str(file)).grid())

    def set_not_repository_available(self, message='Not repository found'):
        self.repo_info = tk.LabelFrame(self, text=message)
        self.repo_info.grid()

        self.left = tk.Label(self.repo_info, text=message)
        self.left.grid()

        self.quitButton = tk.Button(self, text="Cerrar", command=self.quit)
        self.quitButton.grid()


root = Tk()

w = 600
h = 400

#   Se obtienen las dimensiones de la pantalla
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
app = Application(master=root)
app.master.title('Sincronizar archivos')

if platform() == 'Darwin':
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

app.mainloop()
app.destroy()
