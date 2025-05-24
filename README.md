# Task Tracker CLI

A simple command-line task management application written in Python. All local, on your machine.

## 🔧 Requirements

- Python 3.10+
- Click library (for CLI interface)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd task_tracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install click
   ```

## Usage

### Basic Commands

#### Add a Task
```bash
python main.py add "Buy groceries"
python main.py add "Write documentation" --description "Complete the README file"
# Short form:
python main.py add "Review code" -d "Review PR #123"
```

#### View All Tasks
```bash
python main.py view
```

#### View Specific Task
```bash
python main.py view --id 1
# Short form:
python main.py view -i 1
```

#### Complete a Task
```bash
python main.py complete --id 1
# Short form:
python main.py complete -i 1
```

#### Delete a Task
```bash
python main.py delete --id 1
# Short form:
python main.py delete -i 1
```


## Storage Format

Tasks are stored locally in `tasks.json` with the following structure:

```json
{
  "next_id": 3,
  "tasks": {
    "1": {
      "task": "Buy groceries",
      "description": "Get milk, bread, and eggs",
      "completed": false
    },
    "2": {
      "task": "Write documentation", 
      "description": "Complete the README file",
      "completed": true
    }
  }
}
```

##  TODO: 

- Due dates 
- Sorting tasks

