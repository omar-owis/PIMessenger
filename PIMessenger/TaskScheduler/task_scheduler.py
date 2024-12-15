import threading
import time
import typing
from datetime import datetime

class TaskScheduler:
    # TODO: handle termination of threads on object deletion
    def __init__(self):
        self.tasks: dict[str, Task] = {}
    
    def stop(self):
        for _, task in self.tasks.items():
            task.terminate()
    
    def add(self, func: callable, execute_datetime: datetime, task_id: str):
        if datetime.now() > execute_datetime:
            raise ValueError('Past datetime')
        task = self.Task(func, execute_datetime, lambda: self._remove_task(task_id))
        thread = threading.Thread(target=task.begin)
        self.tasks[task_id] = task
        thread.start()
    
    def remove(self,  task_id: str):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.terminate()
            del self.tasks[task_id]
    
    def _remove_task(self, task_id: str):
        del self.tasks[task_id]
        
    
    class Task:
        def __init__(self, function: callable, execute_time: datetime, on_complete: callable, *args, **kwargs):
            # throw execption if execute_time is before today
            self.function = function
            self.execute_time = execute_time
            self.on_complete = on_complete
            self.args = args
            self.kwargs = kwargs
            self._event = threading.Event()
            self._kill = False
        
        def begin(self):
            try:
                wait_period = self._calculate_secs()
                if wait_period > 0:
                    self._event.wait(wait_period)  # maximum TIMEOUT_MAX -> 49.71 days
                
                if not self._kill:
                    self.function(*self.args, **self.kwargs)
                    self.on_complete()
            except Exception as e:
                print(f"Error executing task: {e}")
        
        def terminate(self):
            self._kill = True
            self._event.set()
        
        def _calculate_secs(self):
            now = datetime.now()
            time_difference = self.execute_time - now
            return time_difference.total_seconds()
