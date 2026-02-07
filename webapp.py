from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from typing import Optional

from storage import TaskStore
from task import Task, VALID_CATEGORIES, CAT_IMPORTANT_URGENT, CAT_URGENT, CAT_IMPORTANT, CAT_PARKING_LOT
from week_utils import get_week_start

app = FastAPI(title="Eisenhower Matrix Todo")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

store = TaskStore()

class TaskCreate(BaseModel):
    text: str
    category: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/tasks")
async def get_tasks():
    week_start = get_week_start()
    tasks = store.get_tasks_for_week(week_start)
    # Sort: Category Priority, then Completed, then ID
    # We want to enable the frontend to easily group them
    # For JSON, let's just return the flat list and let frontend handle or pre-sort?
    # Let's pre-sort to be consistent with TUI/CLI logic
    
    # Priority mapping (Lower is higher priority)
    PRIORITY_MAP = {
        CAT_IMPORTANT_URGENT: 1,
        CAT_URGENT: 2,
        CAT_IMPORTANT: 3,
        CAT_PARKING_LOT: 4
    }
    
    tasks.sort(key=lambda t: (PRIORITY_MAP.get(t.category, 99), t.completed, t.id))
    
    return [t.to_dict() for t in tasks]

@app.post("/api/tasks")
async def create_task(task_data: TaskCreate):
    week_start = get_week_start()
    
    # Check limit (only active tasks count)
    # Check limit (only active tasks count)
    count = store.get_task_count_by_category(week_start, task_data.category)
    
    limit = 5 if task_data.category == CAT_PARKING_LOT else 3
    
    if count >= limit:
        raise HTTPException(status_code=400, detail=f"Category is full ({count}/{limit} tasks). Complete existing ones first.")
        
    new_task = Task(task_data.text, category=task_data.category)
    store.add_task(new_task)
    return new_task.to_dict()

@app.post("/api/tasks/{task_id}/toggle")
async def toggle_task(task_id: int):
    tasks = store.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task.completed = not task.completed
    store.save_tasks(tasks)
    return task.to_dict()

class TaskUpdate(BaseModel):
    text: Optional[str] = None
    category: Optional[str] = None

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate):
    week_start = get_week_start()
    tasks = store.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Update text if provided
    if task_data.text is not None:
        task.text = task_data.text
        
    # Update category if provided
    if task_data.category is not None and task_data.category != task.category:
        if task_data.category not in VALID_CATEGORIES:
             raise HTTPException(status_code=400, detail="Invalid category")

        # Check limits if moving to a restricted category
        # Count tasks in target category (excluding the current task if it was already there, which it isn't)
        # We need to count tasks in the *target* category for the *current* week
        # But `store.get_task_count_by_category` loads from file. 
        # We should calculate from our loaded `tasks` list to be safe and atomic-ish?
        # Actually `store` methods read the file.
        # Let's count manually from our `tasks` list which is the current state + modification
        
        target_cat_count = sum(1 for t in tasks 
                               if t.week_start == week_start 
                               and t.category == task_data.category 
                               and not t.completed)
                               
        limit = 5 if task_data.category == CAT_PARKING_LOT else 3
        
        # If the task is being moved *into* this category, checks apply
        if target_cat_count >= limit:
             raise HTTPException(status_code=400, detail=f"Target category is full ({target_cat_count}/{limit}).")
             
        task.category = task_data.category
        
    store.save_tasks(tasks)
    return task.to_dict()

@app.delete("/api/tasks/delete-all")
async def delete_all_tasks():
    week_start = get_week_start()
    tasks = store.load_tasks()
    
    # Keep tasks that are NOT in the current week
    remaining_tasks = [t for t in tasks if t.week_start != week_start]
    deleted_count = len(tasks) - len(remaining_tasks)
    
    if deleted_count > 0:
        store.save_tasks(remaining_tasks)
        
    return {"status": "success", "count": deleted_count}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    tasks = store.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    tasks.remove(task)
    store.save_tasks(tasks)
    return {"status": "success"}

@app.post("/api/tasks/complete-all")
async def complete_all_tasks():
    week_start = get_week_start()
    tasks = store.load_tasks()
    
    count = 0
    for task in tasks:
        if task.week_start == week_start and not task.completed:
            task.completed = True
            count += 1
            
    if count > 0:
        store.save_tasks(tasks)
        
    return {"status": "success", "count": count}



if __name__ == "__main__":
    uvicorn.run("webapp:app", host="127.0.0.1", port=8000, reload=True)
