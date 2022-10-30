from typing import List

from task_data_entry import TaskDataEntry


class TasksDatabase:
    # this database is used mainly for loading task state when loading from a task data file or for
    # saving a task data file
    def __init__(self):
        self.tasks_dict = {}

    def add_tasks(self, tasks: List[TaskDataEntry]):
        for task in tasks:
            if task.category in self.tasks_dict.keys():
                self.tasks_dict[task.category].append(task)
            else:
                self.tasks_dict[task.category] = [task]

    def clear_database(self):
        self.tasks_dict = {}
