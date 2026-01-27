\# AI Agent TODO Manager



A week-based command-line TODO list manager built using AI Agent-assisted development with GSD (Get-Shit-Done) and Claude Code.



\## Features



\- 📅 \*\*Week-based organization\*\*: Tasks automatically organized by Monday-Sunday weeks

\- 💾 \*\*Zero dependencies\*\*: Pure Python standard library

\- ✅ \*\*Complete/uncomplete tasks\*\*: Visual strikethrough for completed items

\- 🗑️ \*\*Delete tasks\*\*: Remove tasks you no longer need

\- 🆔 \*\*UUID-based IDs\*\*: Unique, collision-free task identifiers

\- 💾 \*\*JSON persistence\*\*: Tasks saved to local file



\## Installation

```bash

git clone https://github.com/YOUR\_USERNAME/aiagent-todo-manager.git

cd aiagent-todo-manager

```



No dependencies to install - pure Python!



\## Usage

```bash

\# Add a task

py todo.py add "Buy groceries"



\# List all tasks for current week

py todo.py list



\# Complete a task

py todo.py complete <task-id>



\# Delete a task

py todo.py delete <task-id>



\# Show help

py todo.py --help

```



\## Example

```bash

$ py todo.py add "Buy groceries"

Added task: Buy groceries (ID: 349cef9e-bc25-4a16-9d62-ba31317ff8cb)



$ py todo.py add "Write report"

Added task: Write report (ID: b0e6272d-0d9c-432a-88aa-ac277b511308)



$ py todo.py list

\[349cef9e-bc25-4a16-9d62-ba31317ff8cb] Buy groceries

\[b0e6272d-0d9c-432a-88aa-ac277b511308] Write report



$ py todo.py complete 349cef9e-bc25-4a16-9d62-ba31317ff8cb

Marked complete: Buy groceries



$ py todo.py list

\[349cef9e-bc25-4a16-9d62-ba31317ff8cb] ~~Buy groceries~~

\[b0e6272d-0d9c-432a-88aa-ac277b511308] Write report

```



\## Project Structure

```

├── todo.py           # Main CLI interface

├── task.py           # Task data model

├── storage.py        # JSON persistence layer

├── week\_utils.py     # Week boundary calculations

└── .planning/        # GSD development artifacts

&nbsp;   ├── PROJECT.md

&nbsp;   ├── MILESTONES.md

&nbsp;   └── milestones/

```



\## Development Methodology



Built using \[Get-Shit-Done (GSD)](https://github.com/glittercowboy/get-shit-done) workflow system:

\- Spec-driven development

\- Phase-based execution

\- Atomic git commits

\- AI-assisted code generation



\*\*Stats:\*\*

\- 616 lines of Python

\- 15 requirements validated

\- 2 phases, 3 plans, 7 tasks

\- Built in 1 day

\- v1.0 shipped



\## Technical Details



\- \*\*Language\*\*: Python 3.x

\- \*\*Dependencies\*\*: None (stdlib only)

\- \*\*Storage\*\*: JSON file (`tasks.json`)

\- \*\*Architecture\*\*: Modular (task model, storage, utilities, CLI)



\## Built With



\- \[Claude Code](https://claude.ai/code) - AI coding assistant

\- \[GSD](https://github.com/glittercowboy/get-shit-done) - Meta-prompting workflow system

\- Python standard library



\## License



MIT



\## Acknowledgments



Built as part of a 12-week AI agent development learning journey.

