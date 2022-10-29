import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, S, E, W
from tasks import Tasks


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

        self.morning_tab = ttk.Notebook(self.root_frame)
        self.morning_tab.grid(row=0, column=0, sticky=N + S + E + W)
        self.morning_tab.grid_rowconfigure(1, weight=1)
        self.morning_tab.grid_columnconfigure(1, weight=1)

        self.all_tasks = Tasks(self.morning_tab, task_category_name='ALL')
        self.early_morning_tasks = Tasks(self.morning_tab, task_category_name='Early Morning')
        self.late_morning_tasks = Tasks(self.morning_tab, task_category_name='Late Morning')
        self.early_afternoon_tasks = Tasks(self.morning_tab, task_category_name='Early Afternoon')
        self.late_afternoon_tasks = Tasks(self.morning_tab, task_category_name='Late Afternoon')

        self.morning_tab.add(self.all_tasks.frame, text='ALL')
        self.morning_tab.add(self.early_morning_tasks.frame, text='Early Morning')
        self.morning_tab.add(self.late_morning_tasks.frame, text='Late Morning')
        self.morning_tab.add(self.early_afternoon_tasks.frame, text='Early Afternoon')
        self.morning_tab.add(self.late_afternoon_tasks.frame, text='Late Afternoon')

    #     self.inf_loop()
    #
    #
    # def inf_loop(self):
    #     print(self.early_morning_tasks.task_entries[0]['State'].get())
    #     self.after(1000, self.inf_loop)


