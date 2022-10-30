import tkinter as tk
import tkinter as ttk
from tkinter import N, S, E, W, DISABLED, NORMAL
from typing import List

import custom_fonts
from task_data_entry import TaskDataEntry
from tasks_database import TasksDatabase


class Tasks(ttk.Frame):
    def __init__(self, parent, name: str, tasks_database: TasksDatabase):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = name
        self.tasks_database = tasks_database

        self.frame = ttk.Frame(self.parent)

        self.next_task_row_num = 2

        # tasks
        self.add_more_button = ttk.Button(self.frame, text='ADD', command=self.add_new_task, font=custom_fonts.DEFAULT)
        self.add_more_button.grid(row=1, column=0)

        # load tasks from database
        # if self.tasks_database.tasks_dict.get(name):
        #     tasks = self.tasks_database.tasks_dict[name].copy()
        #     self.set_tasks(tasks)

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

        # add the task to the database
        self.tasks_database.add_tasks(
            [TaskDataEntry(category=self.name, state=check_flag, text=text)]
        )

    # def set_tasks(self, tasks_to_add: List[TaskDataEntry]):
    #     # delete all current task frames
    #     for child in self.frame.winfo_children():
    #         if type(child) is ttk.Frame:
    #             child.destroy()
    #     # create the new frames
    #     for task in tasks_to_add:
    #         self.add_new_task(task.state, task.text)
    #     # create one empty frame if there's none to load
    #     if len(tasks_to_add) == 0:
    #         self.add_new_task()



