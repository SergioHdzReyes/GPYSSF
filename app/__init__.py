import tkinter as tk
from os import system
from platform import system as platform
from app.gui.Application import Application


def create_app():
    root = tk.Tk()

    window_width = 550
    window_height = 450

    #   Se obtienen las dimensiones de la pantalla
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws / 2) - (window_width / 2)
    y = (hs / 2) - (window_height / 2)

    root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    app = Application(master=root)
    app.master.title('Sincronizar archivos')

    if platform() == 'Darwin':
        system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    return app
