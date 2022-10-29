import tkinter as tk
import tkinter as ttk
from tkinter import N, S, E, W, DISABLED, NORMAL

import custom_fonts


class Tasks(ttk.Frame):
    def __init__(self, parent, task_category_name, task_entries=None):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.frame = ttk.Frame(self.parent)

        self.next_task_row_num = 2

        # tasks
        ttk.Label(self.frame, text=task_category_name, font=custom_fonts.DEFAULT).grid(row=0, column=0)
        self.add_more_button = ttk.Button(self.frame, text='ADD', command=self.add_new_task, font=custom_fonts.DEFAULT)
        self.add_more_button.grid(row=1, column=0)

        self.task_entries = []
        if not task_entries:
            self.add_new_task()
        else:
            self.set_tasks(task_entries)

    def add_new_task(self, checkbox_value='0', text_value=''):
        task_frame = ttk.Frame(self.frame)
        task_frame.grid(row=self.next_task_row_num, column=0)
        self.next_task_row_num += 1

        # create entry box
        text = tk.StringVar(value=text_value)
        entry = ttk.Entry(task_frame, textvariable=text, font=custom_fonts.DEFAULT, width=40)
        entry.grid(row=0, column=1)

        def change_entry_state():
            if check_flag.get() == '0':
                entry['state'] = NORMAL
            else:
                entry['state'] = DISABLED

        # completed task checkmark
        check_flag = tk.StringVar(value=checkbox_value)
        ttk.Checkbutton(task_frame, variable=check_flag, font=custom_fonts.DEFAULT, command=change_entry_state)\
            .grid(row=0, column=0)
        entry['state'] = NORMAL if check_flag.get() == '0' else DISABLED

        # create delete button
        ttk.Button(task_frame, text='DEL', font=custom_fonts.DEFAULT, command=lambda: task_frame.grid_forget())\
            .grid(row=0, column=2)

        self.task_entries.append({'State': check_flag, 'Text': text})

    def set_tasks(self, tasks_to_add):
        for task in tasks_to_add:
            state = task['State']
            text = task['Text']
            self.add_new_task(state, text)



