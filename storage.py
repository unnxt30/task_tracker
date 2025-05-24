import json
import os 
from typing import List, Dict, Any 
from datetime import datetime
file_path = 'tasks.json'

def load_tasks() -> Dict[str, Any]:
    """Load tasks from JSON file."""
    if not os.path.exists(file_path):
        return {"next_id": 1, "tasks": {}}
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if "next_id" not in data:
                data["next_id"] = get_max_id(data.get("tasks", {})) + 1
            if "tasks" not in data:
                data["tasks"] = {}
            return data

    except (json.JSONDecodeError, KeyError):
        return {"next_id": 1, "tasks": {}}

def get_max_id(tasks: Dict[str, Any]) -> int:
    if not tasks:
        return 0
    return max(int(task_id) for task_id in tasks.keys())


def get_next_id() -> int:
    data = load_tasks()
    next_id = data['next_id']
    return next_id

def add_task(task: str, description: str = '', due_date: str = f"{datetime.now().strftime('%d-%m-%Y')}") -> None:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({'next_id': 0, 'tasks': {}}, f)

    with open(file_path, 'r') as f:
        data = json.load(f)

    next_id = data['next_id']
    data['tasks'][next_id] = {'task': task, 'description': description, 'completed': False, 'due_date': due_date, 'days_left': calculate_days_left(due_date)}
    data['next_id'] = next_id + 1

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def complete_task(id: int) -> None: 
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({'next_id': 0, 'tasks': {}}, f)

    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if str(id) in data['tasks']:
        data['tasks'][str(id)]['completed'] = True
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def delete_task(id: int) -> None:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({'next_id': 0, 'tasks': {}}, f)

    with open(file_path, 'r') as f:
        data = json.load(f)

    if str(id) in data['tasks']:
        del data['tasks'][str(id)]
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_days_left(due_date: str) -> int:
    today = datetime.now().strftime('%d-%m-%Y')
    res = (datetime.strptime(due_date, '%d-%m-%Y') - datetime.strptime(today, '%d-%m-%Y'))
    return res.days

