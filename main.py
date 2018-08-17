#! /usr/bin/env python
# coding=utf-8
import tkinter as tk
from tkinter import Tk
from tkinter import StringVar
from git import Repo
import os
import sys
from os import system
from platform import system as platform
from configparser import SafeConfigParser
from Directories import Directories

if len(sys.argv) > 1:
    dir_path = sys.argv[1]
    os.chdir(sys.argv[1])
else:
    dir_path = os.path.dirname(os.path.realpath(__file__))

window_width = 550
window_height = 450


class Application(tk.Frame):
    """Clase principal para correr la interfaz de la sincronizacion de archivos"""

    root_dir = ''
    files_with_changes = []
    error_exception = ''
    dirs = None
    config = None
    host_selected = None

    # Widgets
    checkboxes = []
    quit_button = None
    listbox_host = None

    # Frames
    config_frame = None

    def __init__(self, master=None):
        global window_width, window_height
        tk.Frame.__init__(self, master, background='yellow', borderwidth=5, width=100, height=100)
        self.grid()
        self.frames_configuration()

        try:
            self.repo = Repo(dir_path)
        except Exception:
            self.set_not_repository_available()
            return
        self.config = Configuration()

        self.set_repository_information()
        self.create_widgets()

        self.root_dir = dir_path

        self.set_files_with_changes()

        self.dirs = Directories(self.files_with_changes, self.root_dir)
        self.dirs.set_directories_list()

        self.dirs.print_directories_list()

        self.draw_checkbox_files()

    def frames_configuration(self):
        self.config_frame = tk.Frame(self, background='green', borderwidth=2, width=300, height=200)
        self.config_frame.grid()

    def set_repository_information(self):
        self.repo_info = tk.LabelFrame(self, text="Informacion del repositorio")
        self.repo_info.grid()

        branches = [h.name for h in self.repo.heads]

        text = "\nRama actual: " + str(self.repo.active_branch) + \
               "\nRamas: " + str(branches)

        self.left = tk.Label(self.repo_info, text=text)
        self.left.grid()

    def create_widgets(self):
        self.quit_button = tk.Button(self, text="Cerrar", command=self.quit)
        self.quit_button.grid()

        hosts = self.config.get_hosts_list()
        self.host_selected = StringVar(self)
        self.host_selected.set(hosts[0])

        self.listbox_host = tk.OptionMenu(self, self.host_selected, *hosts)
        self.listbox_host.grid()

    def set_files_with_changes(self):
        files = os.popen('git status -s | cut -c4-', 'r')
        self.files_with_changes = files.read().strip().split('\n')
        print('Git status result:')
        print(self.files_with_changes)

    def draw_checkbox_files(self):
        for file in self.dirs.files_with_changes:
            self.checkboxes.append(tk.Checkbutton(self, text=str(file)).grid())

    def set_not_repository_available(self, message='Not repository found'):
        self.repo_info = tk.LabelFrame(self, text=message)
        self.repo_info.grid()

        self.left = tk.Label(self.repo_info, text=message)
        self.left.grid()

        self.quit_button = tk.Button(self, text="Cerrar", command=self.quit)
        self.quit_button.grid()


class Configuration(SafeConfigParser):
    """Clase encargada de administrar las configuraciones"""

    def __init__(self, master=None):
        SafeConfigParser.__init__(self, master)
        self.read('config.ini')

    # Cambia un valor de configuracion
    def add_config(self, section, key, value):
        if not self.has_section(section):
            print('La seccion no existe')
            self.add_section(section)

        self.set(section, key, value)

    # Retorna un valor de configuracion
    def get_config(self, section, key):
        if not self.has_section(section):
            return False

        return self.get(section, key)

    # Obtiene listado de hosts
    def get_hosts_list(self):
        hosts = []
        for key, value in self.items('hosts'):
            hosts.append(value)

        return hosts


root = Tk()

#   Se obtienen las dimensiones de la pantalla
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws/2) - (window_width/2)
y = (hs/2) - (window_height/2)

root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
app = Application(master=root)
app.master.title('Sincronizar archivos')

if platform() == 'Darwin':
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

app.mainloop()
app.destroy()
