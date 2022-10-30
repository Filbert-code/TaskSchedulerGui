import os
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta
from tkinter import N, S, E, W
from typing import List

import custom_fonts
from tasks import Tasks
from tkcalendar import Calendar
from task_data_entry import TaskDataEntry
from tasks_database import TasksDatabase

PATH = os.getcwd()
TASK_DATA_DIR = 'task_data'


class MainFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.root.option_add('*tearOff', False)
        self.root.title('Tasks Scheduler')
        # self.root.rowconfigure(0, weight=1, minsize=300)
        # self.root.columnconfigure(0, weight=1)

        # root frame setup
        self.root_frame = ttk.Frame(self.root)
        self.root_frame.grid(row=0, column=0, sticky=N + S + E + W)
        self.root_frame.grid_rowconfigure(1, weight=1, minsize=300)
        self.root_frame.grid_columnconfigure(1, weight=1)

        # menu setup
        self.menu_bar = tk.Menu(self.root_frame)
        self.menu_file = tk.Menu(self.menu_bar)
        self.root['menu'] = self.menu_bar
        self.menu_bar.add_cascade(menu=self.menu_file, label='File')
        self.menu_file.add_command(label='Save', command=self.save)
        self.menu_file.add_command(label='Load', command=self.load)

        # clock label
        self.selected_date = datetime.now()
        formated_date = self.selected_date.strftime('%A, %b %d')
        self.clock = ttk.Label(self.root_frame, text=formated_date, font=custom_fonts.DEFAULT)
        self.clock.grid(row=0, column=0)

        # tasks notebook setup
        self.notebook_frame = ttk.Notebook(self.root_frame)
        self.notebook_frame.grid(row=1, column=0, sticky=N + S + E + W)

        # setup tasks database
        self.tasks_database = TasksDatabase()

        # load data
        self.task_categories = None
        self.tasks = []
        self.load_data_for_new_day()

    def load_data_for_new_day(self, date=datetime.now().strftime("%m.%d.%Y")):
        data = self.load_task_data_from_file(date)
        self.task_categories = self.get_task_categories(data)
        self.delete_notebook_frames()
        self.tasks = self.create_task_objects(self.task_categories, data)
        self.update_notebook_frames()

    def delete_notebook_frames(self):
        for task_obj in self.tasks:
            self.notebook_frame.forget(task_obj.frame)

    def update_notebook_frames(self):
        for tasks_obj in self.tasks:
            self.notebook_frame.add(tasks_obj.frame, text=tasks_obj.name)

    def load_task_data_from_file(self, date):
        # load task file data from text file
        tasks_dir = os.path.join(PATH, TASK_DATA_DIR)
        tasks_data_filenames = os.listdir(tasks_dir)
        lines = None
        for tasks_filename in tasks_data_filenames:
            if tasks_filename == date + '.txt':
                # load the file data
                with open(os.path.join(tasks_dir, date + '.txt'), 'r') as file_reader:
                    lines = file_reader.read().splitlines()
        if not lines:
            # load default config
            with open(os.path.join(tasks_dir, 'default.txt'), 'r') as file_reader:
                lines = file_reader.read().splitlines()

        data: List[TaskDataEntry] = []
        for line in lines:
            state, text, task_category = line.split(', ')
            data.append(TaskDataEntry(task_category, state, text))

        return data

    def get_task_categories(self, task_data):
        categories = []
        for data in task_data:
            if data.category not in categories:
                categories.append(data.category)
        return categories

    def create_task_objects(self, categories, task_data):
        tasks = [Tasks(self.notebook_frame, name=name, tasks_database=self.tasks_database) for name in categories]
        for task in tasks:
            for data in task_data:
                if data.category == task.name:
                    task.add_new_task(data.state, data.text)
        return tasks

    def save(self):
        date = self.selected_date.strftime("%m.%d.%Y")
        tasks_dir = os.path.join(PATH, TASK_DATA_DIR)

        with open(os.path.join(tasks_dir, date + '.txt'), 'w') as file_writer:
            for category, tasks_list in self.tasks_database.tasks_dict.items():
                for task in tasks_list:
                    line = f'{", ".join([task.state.get(), task.text.get(), task.category])}'
                    file_writer.write(line + '\n')

    def load(self):
        # show a date picker
        newWindow = tk.Toplevel(self.root)
        newWindow.title('Calendar')
        newWindow.geometry("300x300")
        cal = Calendar(
            newWindow,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )

        cal.tag_config('has_tasks', background='#27b317')

        cal.grid(row=0, column=0)
        self.highlight_task_days(cal)

        def handle_load_tasks_click():
            calendar_date = cal.get_date()
            has_task = len(cal.get_calevents(datetime.strptime(calendar_date, "%m/%d/%y"), 'has_tasks')) > 0
            if has_task:
                datetime_date = datetime.strptime(calendar_date, "%m/%d/%y")
                self.tasks_database.clear_database()
                self.load_data_for_new_day(datetime_date.strftime("%m.%d.%Y"))
                # update the date and clock
                self.selected_date = datetime_date
                self.clock['text'] = datetime_date.strftime('%A, %b %d')
                newWindow.destroy()
            else:
                # TODO: Add a message pop up telling user they need to select a green day
                pass

        button = ttk.Button(newWindow, text='Load Tasks', command=handle_load_tasks_click)
        button.grid(row=1, column=0)

    def highlight_task_days(self, cal):
        tasks_dir = os.path.join(PATH, TASK_DATA_DIR)
        tasks_data_filenames = os.listdir(tasks_dir)
        for tasks_filename in tasks_data_filenames:
            if tasks_filename == 'default.txt':
                continue
            date = datetime.strptime(tasks_filename, "%m.%d.%Y.txt")
            cal.calevent_create(date, 'Alex', ['has_tasks'])




    #     self.inf_loop()
    #
    #
    # def inf_loop(self):
    #     print(self.early_morning_tasks.task_entries[0]['State'].get())
    #     self.after(1000, self.inf_loop)


