# 📋 TODOList Project Board

A JSON-based TODO list management system with GitHub project board synchronization.

*"lasciate ogne speranza voi ch'intrate"* - but with better task tracking! 😄

## 🚀 Features

- **JSON-based storage** - All tasks stored in a structured JSON format
- **GitHub Actions integration** - Automatically syncs tasks to GitHub Issues/Project Board
- **Template system** - Pre-built templates for common task types (features, bugs, documentation)
- **Task concatenation** - Easy merging of task lists
- **Priority & status tracking** - Organize tasks by priority and completion status
- **Command-line interface** - Full CLI for task management

## 📖 Usage

### Basic Commands

```bash
# Add a new task
python todo_manager.py add "Task title" --description "Task description" --priority high

# Add task from template
python todo_manager.py template bug --title "Bug: Fix issue" --description "Detailed bug description"

# Update task status  
python todo_manager.py status TASK_ID done

# List all tasks
python todo_manager.py list

# Show summary
python todo_manager.py summary

# Export for GitHub Actions
python todo_manager.py export
```

### Task Templates

Three built-in templates are available:

1. **Feature Template** (`feature`)
   - Default priority: medium
   - Labels: feature, enhancement

2. **Bug Template** (`bug`) 
   - Default priority: high
   - Labels: bug, urgent

3. **Documentation Template** (`documentation`)
   - Default priority: low
   - Labels: documentation

### Task Status Values

- `todo` - Not started
- `in_progress` - Currently being worked on  
- `done` - Completed
- `blocked` - Cannot proceed

### Priority Levels

- `low` - Nice to have
- `medium` - Standard priority
- `high` - Important/urgent

## 🔄 GitHub Integration

The system automatically syncs with GitHub when `todo_list.json` is modified:

1. **Issues Creation** - Each task becomes a GitHub issue with appropriate labels
2. **Status Sync** - Task status maps to issue open/closed state
3. **Project Board** - Issues can be added to GitHub project boards
4. **Automated Reports** - GitHub Actions generates summary reports

## 📁 File Structure

```
todo_list.json          # Main TODO data file
todo_manager.py         # CLI management script  
sync_to_github.py       # GitHub synchronization script
.github/workflows/      # GitHub Actions workflows
```

## 🏗 JSON Structure

```json
{
  "metadata": {
    "version": "1.0",
    "created": "2024-01-01T00:00:00Z", 
    "last_updated": "2024-01-01T00:00:00Z",
    "total_tasks": 0,
    "completed_tasks": 0
  },
  "templates": {
    "feature": { ... },
    "bug": { ... }, 
    "documentation": { ... }
  },
  "tasks": [
    {
      "id": "unique-uuid",
      "title": "Task title",
      "description": "Task description", 
      "priority": "medium",
      "status": "todo",
      "labels": ["tag1", "tag2"],
      "assignee": "",
      "due_date": "",
      "estimated_hours": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## 🔗 Task Concatenation

To merge tasks from another TODO list:

```python
from todo_manager import TODOManager

manager = TODOManager()

# Load external tasks
import json
with open('external_tasks.json', 'r') as f:
    external_data = json.load(f)

# Concatenate tasks  
manager.concatenate_tasks(external_data)
```

## 🤝 Contributing

1. Add your tasks using the CLI or by editing `todo_list.json`
2. Commit changes to trigger GitHub Actions sync
3. Tasks will automatically appear as GitHub issues
4. Use GitHub project boards to organize and track progress

## 📊 Example Workflow

```bash
# Start a new feature
python todo_manager.py template feature --title "Feature: User authentication"

# Update as you work
python todo_manager.py status TASK_ID in_progress

# Mark complete when done  
python todo_manager.py status TASK_ID done

# Generate status report
python todo_manager.py summary
```

The system will automatically sync these changes to your GitHub project board! 🎉
