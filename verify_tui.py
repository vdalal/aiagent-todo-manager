
import asyncio
from tui import TodoApp, CAT_IMPORTANT_URGENT
from storage import TaskStore
import os

async def verify_tui_logic():
    print("--- Starting TUI Logic Verification ---")
    
    # 1. Clean verify
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')
    
    app = TodoApp()
    async with app.run_test() as pilot:
        # 2. Simulate typing a task
        input_widget = app.query_one("#input")
        input_widget.value = "TUI Task 1"
        await pilot.press("enter")
        
        # 3. Check if it's currently stored
        store = TaskStore()
        tasks = store.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].text == "TUI Task 1"
        print("[PASS] Added task via TUI Input")
        
        # 4. Check if widget exists
        # Textual tests might need a pause for refresh?
        # refresh_tasks is synchronous in our code, so it should be there.
        # We look for a Checkbox with the label
        checkboxes = app.query("Checkbox")
        found = False
        for cb in checkboxes:
            if "TUI Task 1" in str(cb.label):
                found = True
                break
        
        if found:
            print("[PASS] Widget appeared in UI")
        else:
            print("[FAIL] Widget not found in UI")

    print("--- TUI Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(verify_tui_logic())
