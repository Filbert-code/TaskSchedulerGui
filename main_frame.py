import tkinter as tk
import tkinter as ttk
from tkinter import N, S, E, W


class MainFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.root.option_add('*tearOff', False)
        self.root.title('Tasks Scheduler')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # root frame setup
        self.root_frame = ttk.Frame(self.root)
        self.root_frame.grid(row=0, column=0, sticky=N + S + E + W)
        self.root_frame.grid_rowconfigure(1, weight=1)
        self.root_frame.grid_columnconfigure(1, weight=1)





