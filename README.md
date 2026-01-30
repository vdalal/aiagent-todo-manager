# AI Agent TODO Manager

A week-based command-line TODO list manager built using AI Agent-assisted development. Now features the **Eisenhower Matrix** for productivity!

## Features

- 📅 **Week-based organization**: Tasks automatically organized by Monday-Sunday weeks
- 🧠 **Eisenhower Matrix**: Categorize tasks by Priority:
    - **Important & Urgent** (Priority 1)
    - **Urgent** (Priority 2)
    - **Important** (Priority 3)
- 🔢 **Simple IDs**: Easy-to-type integer IDs (1, 2, 3...)
- 🚫 **Task Limits**: Strict limit of **3 tasks** per category to enforce focus
- ⚡ **Bulk Actions**: Complete or delete all tasks for the week in one command
- 💾 **Zero dependencies**: Pure Python standard library
- 💾 **JSON persistence**: Tasks saved to local file (`tasks.json`)

## Installation

```bash
git clone https://github.com/vdalal/aiagent-todo-manager.git
cd aiagent-todo-manager
```

No dependencies to install - pure Python!

## Usage

```bash
# Add a task (Default category: Important & Urgent)
py todo.py add "Fix server"

# Add a task to specific category
py todo.py add "Buy milk" -c urgent
py todo.py add "Learn Python" -c important

# List all tasks (Sorted by Priority: Imp+Urg -> Urgent -> Imp)
py todo.py list

# Complete a task
py todo.py complete <id>

# Delete a task
py todo.py delete <id>

# BULK ACTIONS
# Complete ALL tasks for the current week
py todo.py complete-all

# Delete ALL tasks for the current week
py todo.py delete-all

# Show help
py todo.py --help
```

### Valid Categories
- `important_urgent` (Default)
- `urgent`
- `important`

## Example

```bash
$ py todo.py add "Fix critical bug" -c important_urgent
Added task: Fix critical bug (ID: 1) -> Important & Urgent

$ py todo.py add "Email boss" -c urgent
Added task: Email boss (ID: 2) -> Urgent (Not Important)

$ py todo.py list

--- Important & Urgent ---
[1] Fix critical bug

--- Urgent (Not Important) ---
[2] Email boss

$ py todo.py complete 1
Marked complete: Fix critical bug

$ py todo.py list

--- Urgent (Not Important) ---
[2] Email boss

--- Important & Urgent ---
[1] ~~Fix critical bug~~
```

## Project Structure

```
├── todo.py           # Main CLI interface
├── task.py           # Task data model
├── storage.py        # JSON persistence layer
└── week_utils.py     # Week boundary calculations
```

## Technical Details

- **Language**: Python 3.x
- **Dependencies**: None (stdlib only)
- **Storage**: JSON file (`tasks.json`)
- **Key Concepts**: Eisenhower Matrix, Week-based partitioning

## License

MIT
