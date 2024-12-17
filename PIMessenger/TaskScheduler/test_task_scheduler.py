from task_scheduler import TaskScheduler

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import time
import random
from threading import Thread
import threading

class TestTaskScheduler(unittest.TestCase):
    def test_100_tasks_scheduled_at_the_same_time(self):
        scheduler = TaskScheduler()
        tasks = []
        execute_time = datetime.now() + timedelta(seconds=1)  # Tasks will be scheduled 1 second from now

        # Add 100 tasks
        for i in range(100):
            task_id = f"task_{i}"
            func = MagicMock()
            scheduler.add(func, execute_time, task_id)
            tasks.append(func)

        # Wait a moment to allow tasks to "start" (since we've mocked time.sleep)
        time.sleep(1.1)

        # Ensure that each function was called once
        for func in tasks:
            func.assert_called_once()

        self.assertEqual(len(scheduler.tasks), 0)

    def test_scheduler_stop_with_active_tasks(self):
        scheduler = TaskScheduler()
        execute_time = datetime.now() + timedelta(seconds=1)
        func = MagicMock()
    
        # Add one task
        scheduler.add(func, execute_time, "task_1")
        
        scheduler.stop()
    
        # Wait a moment to simulate tasks running
        time.sleep(1.1)
    
        # Check if the function was called
        func.assert_not_called()

    def test_remove_task_and_terminate_thread(self):
        scheduler = TaskScheduler()
        execute_time = datetime.now() + timedelta(seconds=2)
        func = MagicMock()

        # Add task
        scheduler.add(func, execute_time, "task_1")

        # Wait for a moment (so the task is started)
        time.sleep(1)

        # Remove the task
        scheduler.remove("task_1")
        
        # Wait a moment to simulate tasks running
        time.sleep(1.1)

        # Ensure that the task was terminated and function is not called
        func.assert_not_called()

    def test_remove_non_existing_task(self):
        scheduler = TaskScheduler()

        # Remove a task that doesn't exist
        scheduler.remove("non_existing_task")

        # No error should occur and no tasks should be affected.
        self.assertEqual(len(scheduler.tasks), 0)

    def test_invalid_execute_time(self):
        scheduler = TaskScheduler()
        execute_time = datetime.now() - timedelta(days=1)  # Past time, invalid

        with self.assertRaises(ValueError):
            scheduler.add(lambda: None, execute_time, "task_invalid")

    def test_no_execute_time(self):
        scheduler = TaskScheduler()

        with self.assertRaises(TypeError):
            scheduler.add(lambda: None, None, "task_no_time")

    def test_terminate_multiple_times(self):
        scheduler = TaskScheduler()
        execute_time = datetime.now() + timedelta(seconds=1)
        func = MagicMock()
        scheduler.add(func, execute_time, "task_1")

        scheduler.tasks["task_1"].terminate()
        scheduler.tasks["task_1"].terminate()  # Should not raise any errors or have side effects

        # Verify the function was not called
        func.assert_not_called()

    def test_large_number_of_tasks(self):
        scheduler = TaskScheduler()
        execute_time = datetime.now() + timedelta(seconds=random.uniform(1.0, 5.0))
        tasks = []

        for i in range(1000):
            task_id = f"task_{i}"
            func = MagicMock()
            scheduler.add(func, execute_time, task_id)
            tasks.append(func)

        # Ensure all 1000 tasks are scheduled
        self.assertEqual(len(scheduler.tasks), 1000)

        # Wait a moment for all tasks to "start"
        time.sleep(5.1)

        # Ensure that each function was called exactly once
        for func in tasks:
            func.assert_called_once()
        
        # Ensure zero tasks are scheduled
        self.assertEqual(len(scheduler.tasks), 0)

    def test_remove_non_existent_task(self):
        scheduler = TaskScheduler()

        # Try to remove a non-existent task
        scheduler.remove("non_existent_task")

        # Ensure no error occurs, and the scheduler remains intact
        self.assertEqual(len(scheduler.tasks), 0)

    def test_remove_task_before_execution(self):
        scheduler = TaskScheduler()
        execute_time = datetime.now() + timedelta(seconds=1)
        func = MagicMock()

        # Add task
        scheduler.add(func, execute_time, "task_1")

        # Simulate the task is in execution (waiting for some time)
        time.sleep(0.5)

        # Remove task while it's executing
        scheduler.remove("task_1")

        # Wait for the task's scheduled time
        time.sleep(1)

        # Ensure the task was terminated and not executed
        func.assert_not_called()
        self.assertEqual(len(scheduler.tasks), 0)

    def test_thread_safety(self):
        def add_task_thread(scheduler):
            execute_time = datetime.now() + timedelta(seconds=1)
            func = MagicMock()
            scheduler.add(func, execute_time, "task_1")

        def remove_task_thread(scheduler):
            time.sleep(0.5)  # Wait for task to be added
            scheduler.remove("task_1")

        scheduler = TaskScheduler()

        # Run adding and removing tasks in parallel
        add_thread = Thread(target=add_task_thread, args=(scheduler,))
        remove_thread = Thread(target=remove_task_thread, args=(scheduler,))

        add_thread.start()
        remove_thread.start()

        add_thread.join()
        remove_thread.join()

        # Ensure that the task was not added or executed
        self.assertEqual(len(scheduler.tasks), 0)
        
    def test_disable_enable_functionality(self):
        scheduler = TaskScheduler()
        tasks = []
        execute_time = datetime.now() + timedelta(seconds=1)  # Tasks will be scheduled 1 second from now

        # Add 100 tasks
        for i in range(100):
            task_id = f"task_{i}"
            func = MagicMock()
            scheduler.add(func, execute_time, task_id)
            tasks.append(func)

        scheduler.disable()
        time.sleep(1.1)

        # Ensure that each function was not called
        for func in tasks:
            func.assert_not_called()
        
        scheduler.enable()
        time.sleep(0.1)       
        
        # Ensure that each function was called exactly once
        for func in tasks:
            func.assert_called_once()
        
    def test_multiple_disables_enables(self):
        scheduler = TaskScheduler()
        tasks = []
        execute_time = datetime.now() + timedelta(seconds=1)  # Tasks will be scheduled 1 second from now

        # Add 100 tasks
        for i in range(100):
            task_id = f"task_{i}"
            func = MagicMock()
            scheduler.add(func, execute_time, task_id)
            tasks.append(func)

        scheduler.disable()
        time.sleep(0.3)
        scheduler.enable()

        # Ensure that each function was not called
        for func in tasks:
            func.assert_not_called()
        
        scheduler.disable()
        time.sleep(0.5)
        scheduler.enable()

        time.sleep(0.5)
        
        # Ensure that each function was called exactly once
        for func in tasks:
            func.assert_called_once()
    
if __name__ == '__main__':
    unittest.main()