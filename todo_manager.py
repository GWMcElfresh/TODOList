#!/usr/bin/env python3
"""
TODO List Manager - A JSON-based task management system
Manages TODO items with GitHub project board synchronization
"""

import json
import datetime
import uuid
import argparse
import os
from typing import Dict, List, Any, Optional

class TODOManager:
    def __init__(self, file_path: str = "todo_list.json"):
        self.file_path = file_path
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load TODO data from JSON file"""
        if not os.path.exists(self.file_path):
            return self._create_default_structure()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Warning: Could not load {self.file_path}, creating new file")
            return self._create_default_structure()
    
    def _create_default_structure(self) -> Dict[str, Any]:
        """Create default TODO structure"""
        return {
            "metadata": {
                "version": "1.0",
                "created": datetime.datetime.now().isoformat() + "Z",
                "last_updated": datetime.datetime.now().isoformat() + "Z",
                "total_tasks": 0,
                "completed_tasks": 0
            },
            "templates": {
                "feature": {
                    "title": "Feature: [Feature Name]",
                    "description": "Implement [feature description]",
                    "priority": "medium",
                    "status": "todo",
                    "labels": ["feature", "enhancement"],
                    "assignee": "",
                    "due_date": "",
                    "estimated_hours": 0
                },
                "bug": {
                    "title": "Bug: [Bug Description]",
                    "description": "Fix issue with [bug details]",
                    "priority": "high",
                    "status": "todo",
                    "labels": ["bug", "urgent"],
                    "assignee": "",
                    "due_date": "",
                    "estimated_hours": 0
                },
                "documentation": {
                    "title": "Docs: [Documentation Topic]",
                    "description": "Create/update documentation for [topic]",
                    "priority": "low",
                    "status": "todo",
                    "labels": ["documentation"],
                    "assignee": "",
                    "due_date": "",
                    "estimated_hours": 0
                }
            },
            "tasks": []
        }
    
    def _save_data(self) -> None:
        """Save TODO data to JSON file"""
        self.data["metadata"]["last_updated"] = datetime.datetime.now().isoformat() + "Z"
        self.data["metadata"]["total_tasks"] = len(self.data["tasks"])
        self.data["metadata"]["completed_tasks"] = len([
            task for task in self.data["tasks"] if task["status"] == "done"
        ])
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_task(self, title: str, description: str = "", priority: str = "medium", 
                 labels: List[str] = None, assignee: str = "", due_date: str = "",
                 estimated_hours: int = 0) -> str:
        """Add a new task"""
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "todo",
            "labels": labels or [],
            "assignee": assignee,
            "due_date": due_date,
            "estimated_hours": estimated_hours,
            "created_at": datetime.datetime.now().isoformat() + "Z",
            "updated_at": datetime.datetime.now().isoformat() + "Z"
        }
        
        self.data["tasks"].append(task)
        self._save_data()
        return task_id
    
    def add_task_from_template(self, template_name: str, **kwargs) -> str:
        """Add a task from a template"""
        if template_name not in self.data["templates"]:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.data["templates"][template_name].copy()
        
        # Override template values with provided kwargs
        for key, value in kwargs.items():
            if key in template:
                template[key] = value
        
        return self.add_task(
            title=template["title"],
            description=template["description"],
            priority=template["priority"],
            labels=template["labels"],
            assignee=template["assignee"],
            due_date=template["due_date"],
            estimated_hours=template["estimated_hours"]
        )
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status"""
        valid_statuses = ["todo", "in_progress", "done", "blocked"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.datetime.now().isoformat() + "Z"
                self._save_data()
                return True
        return False
    
    def list_tasks(self, status: str = None, priority: str = None) -> List[Dict[str, Any]]:
        """List tasks with optional filtering"""
        tasks = self.data["tasks"]
        
        if status:
            tasks = [task for task in tasks if task["status"] == status]
        
        if priority:
            tasks = [task for task in tasks if task["priority"] == priority]
        
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                return task
        return None
    
    def concatenate_tasks(self, new_tasks_data: Dict[str, Any]) -> None:
        """Concatenate new tasks from another TODO data structure"""
        if "tasks" in new_tasks_data:
            # Generate new IDs for imported tasks to avoid conflicts
            for task in new_tasks_data["tasks"]:
                task["id"] = str(uuid.uuid4())
                task["created_at"] = datetime.datetime.now().isoformat() + "Z"
                task["updated_at"] = datetime.datetime.now().isoformat() + "Z"
            
            self.data["tasks"].extend(new_tasks_data["tasks"])
            self._save_data()
    
    def export_for_github(self) -> Dict[str, Any]:
        """Export data in format suitable for GitHub Actions"""
        return {
            "metadata": self.data["metadata"],
            "tasks": self.data["tasks"],
            "summary": {
                "total": len(self.data["tasks"]),
                "todo": len([t for t in self.data["tasks"] if t["status"] == "todo"]),
                "in_progress": len([t for t in self.data["tasks"] if t["status"] == "in_progress"]),
                "done": len([t for t in self.data["tasks"] if t["status"] == "done"]),
                "blocked": len([t for t in self.data["tasks"] if t["status"] == "blocked"])
            }
        }
    
    def print_summary(self) -> None:
        """Print a summary of tasks"""
        total = len(self.data["tasks"])
        completed = len([t for t in self.data["tasks"] if t["status"] == "done"])
        in_progress = len([t for t in self.data["tasks"] if t["status"] == "in_progress"])
        todo = len([t for t in self.data["tasks"] if t["status"] == "todo"])
        blocked = len([t for t in self.data["tasks"] if t["status"] == "blocked"])
        
        print(f"\n📋 TODO List Summary")
        print(f"{'='*50}")
        print(f"Total tasks: {total}")
        print(f"✅ Completed: {completed}")
        print(f"🔄 In Progress: {in_progress}")
        print(f"📝 Todo: {todo}")
        print(f"🚫 Blocked: {blocked}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"📊 Completion rate: {completion_rate:.1f}%")

def main():
    parser = argparse.ArgumentParser(description="TODO List Manager")
    parser.add_argument("--file", default="todo_list.json", help="JSON file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--description", default="", help="Task description")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    add_parser.add_argument("--labels", nargs="*", default=[], help="Task labels")
    add_parser.add_argument("--assignee", default="", help="Task assignee")
    add_parser.add_argument("--due-date", default="", help="Due date (ISO format)")
    add_parser.add_argument("--hours", type=int, default=0, help="Estimated hours")
    
    # Add from template command
    template_parser = subparsers.add_parser("template", help="Add task from template")
    template_parser.add_argument("template_name", choices=["feature", "bug", "documentation"])
    template_parser.add_argument("--title", help="Override template title")
    template_parser.add_argument("--description", help="Override template description")
    
    # Update status command
    status_parser = subparsers.add_parser("status", help="Update task status")
    status_parser.add_argument("task_id", help="Task ID")
    status_parser.add_argument("new_status", choices=["todo", "in_progress", "done", "blocked"])
    
    # List tasks command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["todo", "in_progress", "done", "blocked"])
    list_parser.add_argument("--priority", choices=["low", "medium", "high"])
    
    # Summary command
    subparsers.add_parser("summary", help="Show task summary")
    
    # Export command
    subparsers.add_parser("export", help="Export for GitHub Actions")
    
    args = parser.parse_args()
    
    manager = TODOManager(args.file)
    
    if args.command == "add":
        task_id = manager.add_task(
            title=args.title,
            description=args.description,
            priority=args.priority,
            labels=args.labels,
            assignee=getattr(args, 'assignee', ''),
            due_date=getattr(args, 'due_date', ''),
            estimated_hours=args.hours
        )
        print(f"✅ Added task: {task_id}")
    
    elif args.command == "template":
        kwargs = {}
        if args.title:
            kwargs["title"] = args.title
        if args.description:
            kwargs["description"] = args.description
        
        task_id = manager.add_task_from_template(args.template_name, **kwargs)
        print(f"✅ Added task from template '{args.template_name}': {task_id}")
    
    elif args.command == "status":
        success = manager.update_task_status(args.task_id, args.new_status)
        if success:
            print(f"✅ Updated task {args.task_id} to '{args.new_status}'")
        else:
            print(f"❌ Task {args.task_id} not found")
    
    elif args.command == "list":
        tasks = manager.list_tasks(status=args.status, priority=args.priority)
        for task in tasks:
            status_emoji = {"todo": "📝", "in_progress": "🔄", "done": "✅", "blocked": "🚫"}
            priority_emoji = {"low": "🔵", "medium": "🟡", "high": "🔴"}
            print(f"{status_emoji.get(task['status'], '❓')} {priority_emoji.get(task['priority'], '⚪')} {task['title']}")
            print(f"   ID: {task['id']}")
            if task['description']:
                print(f"   Description: {task['description']}")
            print()
    
    elif args.command == "summary":
        manager.print_summary()
    
    elif args.command == "export":
        export_data = manager.export_for_github()
        print(json.dumps(export_data, indent=2))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()