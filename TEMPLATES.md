# 📋 Task Templates for Copy-Paste

This document provides ready-to-use JSON templates for common task types. Copy and paste these into your TODO list for quick task creation.

## 🚀 Feature Template

```json
{
  "id": "REPLACE_WITH_UUID",
  "title": "Feature: [Feature Name]",
  "description": "Implement [feature description]",
  "priority": "medium",
  "status": "todo", 
  "labels": ["feature", "enhancement"],
  "assignee": "",
  "due_date": "",
  "estimated_hours": 0,
  "created_at": "REPLACE_WITH_TIMESTAMP",
  "updated_at": "REPLACE_WITH_TIMESTAMP"
}
```

## 🐛 Bug Fix Template

```json
{
  "id": "REPLACE_WITH_UUID", 
  "title": "Bug: [Bug Description]",
  "description": "Fix issue with [bug details]",
  "priority": "high",
  "status": "todo",
  "labels": ["bug", "urgent"],
  "assignee": "",
  "due_date": "",
  "estimated_hours": 0,
  "created_at": "REPLACE_WITH_TIMESTAMP",
  "updated_at": "REPLACE_WITH_TIMESTAMP"
}
```

## 📚 Documentation Template

```json
{
  "id": "REPLACE_WITH_UUID",
  "title": "Docs: [Documentation Topic]", 
  "description": "Create/update documentation for [topic]",
  "priority": "low",
  "status": "todo",
  "labels": ["documentation"],
  "assignee": "",
  "due_date": "",
  "estimated_hours": 0,
  "created_at": "REPLACE_WITH_TIMESTAMP",
  "updated_at": "REPLACE_WITH_TIMESTAMP"  
}
```

## 🔧 Maintenance Template

```json
{
  "id": "REPLACE_WITH_UUID",
  "title": "Maintenance: [Task Description]",
  "description": "Perform maintenance task: [details]", 
  "priority": "medium",
  "status": "todo",
  "labels": ["maintenance", "tech-debt"],
  "assignee": "",
  "due_date": "",
  "estimated_hours": 0,
  "created_at": "REPLACE_WITH_TIMESTAMP",
  "updated_at": "REPLACE_WITH_TIMESTAMP"
}
```

## 🧪 Testing Template  

```json
{
  "id": "REPLACE_WITH_UUID",
  "title": "Test: [Test Description]",
  "description": "Create tests for [component/feature]",
  "priority": "medium", 
  "status": "todo",
  "labels": ["testing", "quality-assurance"],
  "assignee": "",
  "due_date": "",
  "estimated_hours": 0,
  "created_at": "REPLACE_WITH_TIMESTAMP",
  "updated_at": "REPLACE_WITH_TIMESTAMP"
}
```

## 📋 Meeting/Review Template

```json
{
  "id": "REPLACE_WITH_UUID",
  "title": "Meeting: [Meeting Topic]",
  "description": "Attend/organize meeting about [topic]",
  "priority": "medium",
  "status": "todo",
  "labels": ["meeting", "review"],
  "assignee": "", 
  "due_date": "",
  "estimated_hours": 1,
  "created_at": "REPLACE_WITH_TIMESTAMP", 
  "updated_at": "REPLACE_WITH_TIMESTAMP"
}
```

## ✨ How to Use Templates

### Method 1: CLI (Recommended)
```bash
# Use built-in templates
python todo_manager.py template feature --title "Feature: User authentication"
python todo_manager.py template bug --title "Bug: Login validation issue"
```

### Method 2: Direct JSON Editing
1. Copy the template JSON above
2. Replace placeholder values:
   - `REPLACE_WITH_UUID` → Generate a UUID (or let concatenation handle it)
   - `REPLACE_WITH_TIMESTAMP` → Current ISO timestamp
   - `[Bracketed text]` → Your specific details
3. Add to the `tasks` array in `todo_list.json`

### Method 3: Python Script
```python
from todo_manager import TODOManager
import uuid
import datetime

manager = TODOManager()

# Add custom task
task_id = manager.add_task(
    title="Custom: My Task",
    description="Task description here", 
    priority="high",
    labels=["custom", "important"],
    estimated_hours=5
)
```

## 🔄 Task Status Values

- `todo` - Not started
- `in_progress` - Currently being worked on
- `done` - Completed  
- `blocked` - Cannot proceed

## 📊 Priority Levels

- `low` - Nice to have, no rush
- `medium` - Standard priority
- `high` - Important, should be done soon

## 🏷 Common Label Suggestions

- **Type**: `feature`, `bug`, `documentation`, `maintenance`, `testing`
- **Priority**: `urgent`, `critical`, `enhancement`
- **Category**: `frontend`, `backend`, `database`, `security`, `performance`
- **Status**: `blocked`, `in-review`, `needs-testing`