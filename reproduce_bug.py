import os
import sys
from storage import TaskStore
from task import Task, CAT_IMPORTANT_URGENT
from week_utils import get_week_start

def reproduce():
    # Use a test file to avoid messing up real data
    test_file = 'test_tasks.json'
    if os.path.exists(test_file):
        os.remove(test_file)
    
    store = TaskStore(test_file)
    current_week = get_week_start()
    
    print("Step 1: Adding 3 tasks...")
    for i in range(3):
        task = Task(f"Task {i}", category=CAT_IMPORTANT_URGENT)
        store.add_task(task)
    
    count = store.get_task_count_by_category(current_week, CAT_IMPORTANT_URGENT)
    print(f"Count after adding 3: {count}")
    
    print("Step 2: Completing the first task...")
    tasks = store.load_tasks()
    tasks[0].completed = True
    store.save_tasks(tasks)
    
    print("Step 3: Checking count (should be 2, but likely 3 if bug exists)...")
    count = store.get_task_count_by_category(current_week, CAT_IMPORTANT_URGENT)
    print(f"Current count logic returned: {count}")
    
    if count == 3:
        print("FAIL: The bug is present. Completed tasks are being counted.")
    else:
        print("PASS: Completed tasks are NOT being counted.")

if __name__ == "__main__":
    reproduce()
