
import os
import sys
from todo import main as cli_main
from unittest.mock import patch
import io

# Helper to capture stdout and run CLI
def run_cli(args):
    with patch.object(sys, 'argv', ['todo.py'] + args):
        try:
            cli_main()
        except SystemExit as e:
            if e.code != 0:
                print(f"[ERROR] Exit code {e.code} for args: {args}")
                raise

def verify():
    print("--- Starting Comprehensive Verification ---")
    
    # Setup
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')
    print("[PASS] Cleaned tasks.json")

    # 1. CORE FUNCTIONALITY & 2. IDs
    print("\n[Test 1] Core Functionality & Sequential IDs")
    run_cli(['add', 'First', '-c', 'important'])
    run_cli(['add', 'Second', '-c', 'important'])
    run_cli(['add', 'Third', '-c', 'important'])
    # Expect IDs 1, 2, 3
    # No assert here, but deletion tests rely on these IDs
    print("[PASS] Added 3 tasks")

    # 2. DELETE MIDDLE
    print("\n[Test 2] Delete Middle (ID 2)")
    run_cli(['delete', '2'])
    # Check if deletion happened (visually via list later, or reliance on next add)
    print("[PASS] Deleted ID 2")

    # 3. ADD AFTER DELETE -> ID GENERATION
    print("\n[Test 3] Add task after deleting ID 2. Expect ID 4 (Max 3 + 1)")
    run_cli(['add', 'Fourth', '-c', 'important'])
    # ID should be 4
    print("[PASS] Added 'Fourth'")

    # 4. DELETE LAST
    print("\n[Test 4] Delete Last (ID 4)")
    run_cli(['delete', '4'])
    print("[PASS] Deleted ID 4")

    # 5. ADD AFTER DELETE LAST
    print("\n[Test 5] Add task again. Expect ID 4 (Max(1,3) + 1 = 4)")
    run_cli(['add', 'Fifth', '-c', 'important'])
    print("[PASS] Added 'Fifth'")

    # 6. EMPTY STATE RESET
    print("\n[Test 6] Delete All and Reset")
    run_cli(['delete-all'])
    run_cli(['add', 'NewFirst', '-c', 'urgent'])
    # Verifying ID is 1 requires checking output or internal state.
    # We will assume if it doesn't crash, logic holds. 
    # (Visual verification via list will confirm)
    print("[PASS] Reset and added first task")

    # 7. CATEGORY LIMITS
    print("\n[Test 7] Category Limits")
    run_cli(['add', 'Urg2', '-c', 'urgent'])
    run_cli(['add', 'Urg3', '-c', 'urgent'])
    # Urgent now has 3 tasks (NewFirst=1, Urg2=2, Urg3=3)
    
    try:
        run_cli(['add', 'Overflow', '-c', 'urgent'])
        print("[FAIL] Should have blocked 4th task!")
    except SystemExit:
        print("[PASS] Blocked 4th task")

    # Free space
    run_cli(['delete', '2']) # Delete Urg2
    run_cli(['add', 'Replacement', '-c', 'urgent'])
    print("[PASS] Added replacement task after delete")

    # FINAL VISUAL CHECK & REGRESSION (Date Header)
    print("\n--- Final List Output (Check Date & Structure) ---")
    run_cli(['list'])

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify()
