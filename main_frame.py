import os
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import N, S, E, W
from tasks import Tasks
from tkcalendar import Calendar

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
        self.history = self.load_history()

        # root frame setup
        self.root_frame = ttk.Frame(self.root)
        self.root_frame.grid(row=0, column=0, sticky=N + S + E + W)
        self.root_frame.grid_rowconfigure(0, weight=1, minsize=300)
        self.root_frame.grid_columnconfigure(0, weight=1)

        # menu setup
        self.menu_bar = tk.Menu(self.root_frame)
        self.menu_file = tk.Menu(self.menu_bar)
        self.root['menu'] = self.menu_bar
        self.menu_bar.add_cascade(menu=self.menu_file, label='File')
        self.menu_file.add_command(label='Save', command=self.save)
        self.menu_file.add_command(label='Load')

        # tasks notebook setup
        self.morning_tab = ttk.Notebook(self.root_frame)
        self.morning_tab.grid(row=0, column=0, sticky=N + S + E + W)

        self.early_morning_tasks = Tasks(self.morning_tab, task_category_name='Early Morning', task_entries=self.history['Early Morning'])
        self.late_morning_tasks = Tasks(self.morning_tab, task_category_name='Late Morning', task_entries=self.history['Late Morning'])
        self.early_afternoon_tasks = Tasks(self.morning_tab, task_category_name='Early Afternoon', task_entries=self.history['Early Afternoon'])
        self.late_afternoon_tasks = Tasks(self.morning_tab, task_category_name='Late Afternoon', task_entries=self.history['Late Afternoon'])

        self.task_data = [
            (self.early_morning_tasks.task_entries, 'Early Morning'),
            (self.late_morning_tasks.task_entries, 'Late Morning'),
            (self.early_afternoon_tasks.task_entries, 'Early Afternoon'),
            (self.late_afternoon_tasks.task_entries, 'Late Afternoon'),
        ]

        self.morning_tab.add(self.early_morning_tasks.frame, text='Early Morning')
        self.morning_tab.add(self.late_morning_tasks.frame, text='Late Morning')
        self.morning_tab.add(self.early_afternoon_tasks.frame, text='Early Afternoon')
        self.morning_tab.add(self.late_afternoon_tasks.frame, text='Late Afternoon')

        # set the list for all tasks

    def load_history(self):
        todays_date = datetime.now().strftime("%m.%d.%Y")
        tasks_dir = os.path.join(PATH, TASK_DATA_DIR)
        tasks_data_filenames = os.listdir(tasks_dir)
        for tasks_filename in tasks_data_filenames:
            if tasks_filename == todays_date + '.txt':
                # load the file data
                with open(os.path.join(tasks_dir, todays_date + '.txt'), 'r') as file_reader:
                    lines = file_reader.read().splitlines()

        data = {'Early Morning': [], 'Late Morning': [], 'Early Afternoon': [], 'Late Afternoon': []}
        for line in lines:
            state, text, task_category = line.split(', ')
            for key, value in data.items():
                if task_category == key:
                    data[key].append({
                        'State': state,
                        'Text': text,
                    })
        return data

    def save(self):
        todays_date = datetime.now().strftime("%m.%d.%Y")
        tasks_dir = os.path.join(PATH, TASK_DATA_DIR)

        lines = []
        for data, task_category in self.task_data:
            lines += self.convert_task_data_to_save_file_format(data, task_category)

        with open(os.path.join(tasks_dir, todays_date + '.txt'), 'w') as file_writer:
            file_writer.write('\n'.join(lines))

    def convert_task_data_to_save_file_format(self, task_data, task_category):
        return [f'{", ".join([task["State"].get(), task["Text"].get(), task_category])}' for task in task_data]

    def load(self):
        pass


    #     self.inf_loop()
    #
    #
    # def inf_loop(self):
    #     print(self.early_morning_tasks.task_entries[0]['State'].get())
    #     self.after(1000, self.inf_loop)


