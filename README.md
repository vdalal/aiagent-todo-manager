# AI Agent TODO Manager

A week-based task manager featuring the **Eisenhower Matrix** and a modern Web GUI. Built with Python, FastAPI, and vanilla HTML/CSS.

## Features

### 🖥️ Modern Web GUI
- **Visual Dashboard**: Dark-themed, glassmorphism-inspired interface.
- **Eisenhower Matrix**: Tasks automatically sorted into quadrants:
    - **Do First** (Important & Urgent)
    - **Schedule** (Urgent)
    - **Delegate / Later** (Important)
- **Parking Lot**: A 4th column for tasks that don't fit elsewhere, with a dedicated limit of **5 tasks**.
- **Task Limits**: Strict limit of **3 active tasks** for standard categories to enforce focus.
- **Interactive**: 
    - Toggle completion with a click.
    - Rename column headers (e.g., "Do First" -> "Critical") just by clicking them.
    - Delete tasks instantly.
- **Bulk Actions**: Buttons to "Complete Week" or "Delete Week" in one go.

### ⚙️ Core Features
- **Week-based organization**: Tasks automatically partitioned by week.
- **Persistence**: Data saved to `tasks.json`.
- **Zero-Refresh**: Tasks add/delete instantly without full page reloads.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/vdalal/aiagent-todo-manager.git
    cd aiagent-todo-manager
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Start the web server:

```bash
py -m uvicorn webapp:app --reload
```

Open your browser to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## Categories & Limits

| Category | UI Name | Active Limit |
| :--- | :--- | :--- |
| `important_urgent` | Do First | 3 |
| `urgent` | Schedule | 3 |
| `important` | Delegate | 3 |
| `parking_lot` | Parking Lot | **5** |

*Note: Completed tasks do not count towards the active limit.*

## Project Structure

```
├── webapp.py           # FastAPI backend
├── templates/
│   └── index.html      # Frontend HTML
├── static/
│   └── style.css       # CSS Styling
├── todo.py             # (Legacy) CLI interface
├── task.py             # Task data model
└── storage.py          # JSON persistence layer
```

## Technical Details

- **Backend**: Python 3.x, FastAPI
- **Frontend**: HTML5, CSS3 (Grid/Flexbox), Vanilla JS
- **Storage**: JSON file (`tasks.json`)

## License

MIT
