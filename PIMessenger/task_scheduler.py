import threading
import time

class Task:
    def __init__(self, function):
        self.function = function
    
    def get_id(self):
        return id(self)
    

class TaskScheduler:
    def __init__(self):
        pass
    
    def add(self, task, execute_datetime):
        pass
    
    def remove(self, task):
        pass
