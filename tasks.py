import tkinter as tk
import tkinter as ttk
from tkinter import N, S, E, W, DISABLED, NORMAL

import custom_fonts


class Tasks(ttk.Frame):
    def __init__(self, parent, task_category_name):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.frame = ttk.Frame(self.parent)

        self.task_entries = []
        self.next_task_row_num = 2

        # tasks
        ttk.Label(self.frame, text=task_category_name, font=custom_fonts.DEFAULT).grid(row=0, column=0)
        self.add_more_button = ttk.Button(self.frame, text='ADD', command=self.add_new_task, font=custom_fonts.DEFAULT)
        self.add_more_button.grid(row=1, column=0)

        # create first empty task
        self.add_new_task()

    def add_new_task(self):
        task_frame = ttk.Frame(self.frame)
        task_frame.grid(row=self.next_task_row_num, column=0)
        self.next_task_row_num += 1

        # create entry box
        text = tk.StringVar()
        entry = ttk.Entry(task_frame, textvariable=text, font=custom_fonts.DEFAULT, width=40)
        entry.grid(row=0, column=1)

        def change_entry_state():
            if entry['state'] == NORMAL:
                entry['state'] = DISABLED
            else:
                entry['state'] = NORMAL

        # completed task checkmark
        check_flag = tk.StringVar(value='0')
        ttk.Checkbutton(task_frame, variable=check_flag, font=custom_fonts.DEFAULT, command=change_entry_state)\
            .grid(row=0, column=0)

        # create delete button
        ttk.Button(task_frame, text='DEL', font=custom_fonts.DEFAULT, command=lambda: task_frame.grid_forget())\
            .grid(row=0, column=2)

        self.task_entries.append({'State': check_flag, 'Text': text})

    # def set_tasks(self, tasks_frames):
    #     for index, frame in enumerate(tasks_frames):

