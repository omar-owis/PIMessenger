import threading
import time
import typing
from datetime import datetime

class TaskScheduler:
    # TODO: handle termination of threads on object deletion
    def __init__(self):
        self.tasks: dict[str, Task] = {}
    
    def stop(self):
        for task in self.tasks.values():
            task.terminate()
    
    def add(self, func: callable, execute_datetime: datetime, task_id: str):
        if datetime.now() > execute_datetime:
            raise ValueError('Execute datetime must be in the future')
        task = self.Task(func, execute_datetime, lambda: self._remove_task(task_id))
        thread = threading.Thread(target=task.begin, daemon=True)
        self.tasks[task_id] = task
        thread.start()
    
    def remove(self,  task_id: str):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.terminate()
            del self.tasks[task_id]
            
    def disable(self):
        for task in self.tasks.values():
            task.disable()
    
    def enable(self):
        for task in self.tasks.values():
            task.enable()
    
    def _remove_task(self, task_id: str):
        self.tasks.pop(task_id)
        
    
    class Task:
        def __init__(self, function: callable, execute_time: datetime, on_complete: callable, *args, **kwargs):
            # throw execption if execute_time is before today
            self.function = function
            self.execute_time = execute_time
            self.on_complete = on_complete
            self.args = args
            self.kwargs = kwargs
            self._sleep_event = threading.Event()
            self._hold_event = threading.Event()
            self._kill = False
            self._disabled = False
        
        def begin(self):
            try:
                wait_period = self._calculate_secs()
                if wait_period > 0:
                    self._sleep_event.wait(wait_period)  # maximum TIMEOUT_MAX -> 49.71 days
                
                if not self._kill:
                    if self._disabled:
                        self._hold_event.wait()
                    self.function(*self.args, **self.kwargs)
                    self.on_complete()
            except Exception as e:
                print(f"Error executing task: {e}")
        
        def terminate(self):
            self._kill = True
            self._sleep_event.set()
            
        def disable(self):
            self._disabled = True
            self._hold_event.clear()
        
        def enable(self):
            self._disabled = False
            self._hold_event.set()
        
        def _calculate_secs(self):
            now = datetime.now()
            time_difference = self.execute_time - now
            return time_difference.total_seconds()
