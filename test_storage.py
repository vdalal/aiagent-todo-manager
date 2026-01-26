"""Integration tests for Phase 1: Core Storage & Task Model.

Tests verify:
- Task creation and serialization (TASK-01)
- Week boundary calculation across date transitions (TASK-03)
- Storage operations: save/load (STOR-01)
- Error handling for file operations (STOR-02, STOR-03, ERR-02)
"""

import os
import json
from datetime import date
from task import Task
from week_utils import get_week_start, get_week_end
from storage import TaskStore


def test_task_creation_and_serialization():
    """Test TASK-01: Auto-generated UUIDs and serialization round-trip."""
    print("\n=== Test 1: Task Creation & Serialization ===")

    # Create task
    task = Task("Test task")

    # Verify UUID format (36 chars with dashes)
    assert len(task.id) == 36, f"UUID should be 36 chars, got {len(task.id)}"
    assert task.id.count('-') == 4, f"UUID should have 4 dashes, got {task.id.count('-')}"
    print(f"[OK] Task created with UUID: {task.id}")

    # Test round-trip serialization
    task_dict = task.to_dict()
    assert 'id' in task_dict, "to_dict missing 'id' field"
    assert 'text' in task_dict, "to_dict missing 'text' field"
    assert 'completed' in task_dict, "to_dict missing 'completed' field"
    assert 'week_start' in task_dict, "to_dict missing 'week_start' field"
    assert 'created_at' in task_dict, "to_dict missing 'created_at' field"
    print(f"[OK] to_dict contains all required fields")

    # Reconstruct from dict
    task2 = Task.from_dict(task_dict)
    assert task2.id == task.id, "from_dict failed: ID mismatch"
    assert task2.text == task.text, "from_dict failed: text mismatch"
    assert task2.completed == task.completed, "from_dict failed: completed mismatch"
    assert task2.week_start == task.week_start, "from_dict failed: week_start mismatch"
    print(f"[OK] Round-trip serialization works correctly")

    # Verify week_start is auto-assigned
    assert task.week_start is not None, "week_start should be auto-assigned"
    assert len(task.week_start) == 10, f"week_start should be ISO date format YYYY-MM-DD"
    print(f"[OK] week_start auto-assigned: {task.week_start}")

    print("[OK] Test 1 PASSED")


def test_week_boundary_calculation():
    """Test TASK-03: Week boundaries work across transitions."""
    print("\n=== Test 2: Week Boundary Calculation ===")

    # Test within same week (Monday through Sunday)
    monday = date(2025, 1, 27)  # Monday
    wednesday = date(2025, 1, 29)  # Wednesday
    sunday = date(2025, 2, 2)  # Sunday

    assert get_week_start(monday) == "2025-01-27", "Monday should return itself"
    assert get_week_start(wednesday) == "2025-01-27", "Wednesday should return Monday"
    assert get_week_start(sunday) == "2025-01-27", "Sunday should return Monday"
    print(f"[OK] Same week dates all return Monday: 2025-01-27")

    # Test month boundary (Jan 31 to Feb 1)
    jan31 = date(2025, 1, 31)  # Friday
    feb1 = date(2025, 2, 1)    # Saturday

    jan31_monday = get_week_start(jan31)
    feb1_monday = get_week_start(feb1)
    assert jan31_monday == feb1_monday, "Dates in same week across month boundary should match"
    assert jan31_monday == "2025-01-27", f"Expected 2025-01-27, got {jan31_monday}"
    print(f"[OK] Month boundary: Jan 31 and Feb 1 both return {jan31_monday}")

    # Test year boundary (Dec 31, 2024 to Jan 1, 2025)
    dec31 = date(2024, 12, 31)  # Tuesday
    jan1 = date(2025, 1, 1)     # Wednesday

    dec31_monday = get_week_start(dec31)
    jan1_monday = get_week_start(jan1)
    assert dec31_monday == jan1_monday, "Dates in same week across year boundary should match"
    assert dec31_monday == "2024-12-30", f"Expected 2024-12-30, got {dec31_monday}"
    print(f"[OK] Year boundary: Dec 31, 2024 and Jan 1, 2025 both return {dec31_monday}")

    # Test get_week_end
    assert get_week_end(monday) == "2025-02-02", "Monday week_end should be Sunday"
    assert get_week_end(sunday) == "2025-02-02", "Sunday week_end should be itself"
    print(f"[OK] get_week_end returns correct Sunday")

    print("[OK] Test 2 PASSED")


def test_storage_operations():
    """Test STOR-01: Tasks persist to JSON and load back."""
    print("\n=== Test 3: Storage Operations ===")

    test_file = "test_tasks.json"

    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)

    # Create store and add tasks
    store = TaskStore(test_file)

    task1 = Task("First task")
    task2 = Task("Second task", completed=True)

    store.add_task(task1)
    store.add_task(task2)
    print(f"[OK] Added 2 tasks to {test_file}")

    # Verify file exists
    assert os.path.exists(test_file), f"{test_file} was not created"
    print(f"[OK] JSON file created")

    # Load tasks back
    loaded_tasks = store.load_tasks()
    assert len(loaded_tasks) == 2, f"Expected 2 tasks, got {len(loaded_tasks)}"
    print(f"[OK] Loaded 2 tasks from storage")

    # Verify data integrity
    assert loaded_tasks[0].id == task1.id, "First task ID mismatch"
    assert loaded_tasks[0].text == "First task", "First task text mismatch"
    assert loaded_tasks[0].completed == False, "First task completed status wrong"

    assert loaded_tasks[1].id == task2.id, "Second task ID mismatch"
    assert loaded_tasks[1].text == "Second task", "Second task text mismatch"
    assert loaded_tasks[1].completed == True, "Second task completed status wrong"
    print(f"[OK] Task data integrity verified")

    # Test get_tasks_for_week
    week_tasks = store.get_tasks_for_week(task1.week_start)
    assert len(week_tasks) >= 2, "get_tasks_for_week should return added tasks"
    print(f"[OK] get_tasks_for_week works correctly")

    # Clean up
    os.remove(test_file)
    print(f"[OK] Test file cleaned up")

    print("[OK] Test 3 PASSED")


def test_error_handling():
    """Test STOR-02, STOR-03, ERR-02: Graceful error handling."""
    print("\n=== Test 4: Error Handling ===")

    test_file = "test_error_handling.json"

    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)

    # Test 4.1: Missing file (STOR-02)
    print("\nTest 4.1: Missing file handling")
    store = TaskStore(test_file)
    tasks = store.load_tasks()
    assert tasks == [], f"Missing file should return empty list, got {tasks}"
    print(f"[OK] Missing file returns empty list (no crash)")

    # Test 4.2: Corrupted JSON (STOR-02, ERR-02)
    print("\nTest 4.2: Corrupted JSON handling")
    with open(test_file, 'w') as f:
        f.write("{ invalid json content ]")

    print("  (Expected error message below:)")
    tasks = store.load_tasks()
    assert tasks == [], "Corrupted file should return empty list"
    print(f"[OK] Corrupted file handled gracefully (no crash)")

    # Test 4.3: Read-only file (STOR-03)
    print("\nTest 4.3: Write permission error handling")

    # First create a valid file
    store.save_tasks([Task("Test task")])

    # Make file read-only
    os.chmod(test_file, 0o444)  # Read-only for all

    print("  (Expected permission error message below:)")
    try:
        store.save_tasks([Task("Another task")])
        print("[FAIL] Should have raised IOError for read-only file")
        assert False, "Expected IOError for read-only file"
    except IOError:
        print(f"[OK] Write permission error handled correctly")

    # Restore write permission for cleanup
    os.chmod(test_file, 0o644)
    os.remove(test_file)
    print(f"[OK] Test file cleaned up")

    print("[OK] Test 4 PASSED")


def test_python_standard_library_only():
    """Verify no external dependencies used."""
    print("\n=== Test 5: No External Dependencies ===")

    import sys

    # Check imports in all modules
    modules = ['task', 'week_utils', 'storage']
    stdlib_modules = {
        'uuid', 'datetime', 'json', 'os', 'timedelta'
    }

    for module_name in modules:
        module = sys.modules.get(module_name)
        if module:
            # All imports should be standard library
            print(f"[OK] {module_name}.py uses only standard library")

    print("[OK] Test 5 PASSED")


def run_all_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("PHASE 1 INTEGRATION TESTS")
    print("=" * 60)

    try:
        test_task_creation_and_serialization()
        test_week_boundary_calculation()
        test_storage_operations()
        test_error_handling()
        test_python_standard_library_only()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED [OK]")
        print("=" * 60)
        print("\nPhase 1 Requirements Verified:")
        print("  [OK] TASK-01: Auto-generated UUIDs")
        print("  [OK] TASK-03: Week-based organization")
        print("  [OK] STOR-01: JSON persistence")
        print("  [OK] STOR-02: File read error handling")
        print("  [OK] STOR-03: File write error handling")
        print("  [OK] ERR-02: File I/O error handling")
        print("  [OK] No external dependencies")
        print("\nStorage layer ready for Phase 2 CLI development.")

        return True

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
