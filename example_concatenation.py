#!/usr/bin/env python3
"""
Example script demonstrating task concatenation functionality
This shows how to merge TODO lists from multiple sources
"""

import json
from todo_manager import TODOManager

def create_sample_external_tasks():
    """Create sample external tasks to demonstrate concatenation"""
    external_tasks = {
        "tasks": [
            {
                "id": "temp-1",  # This will be replaced with new UUID
                "title": "Review security policies", 
                "description": "Audit and update security policies for the project",
                "priority": "high",
                "status": "todo",
                "labels": ["security", "policy"],
                "assignee": "",
                "due_date": "2024-02-15",
                "estimated_hours": 4
            },
            {
                "id": "temp-2",  # This will be replaced with new UUID
                "title": "Optimize database queries",
                "description": "Improve performance of slow database operations",
                "priority": "medium", 
                "status": "todo",
                "labels": ["performance", "database"],
                "assignee": "",
                "due_date": "",
                "estimated_hours": 8
            },
            {
                "id": "temp-3",  # This will be replaced with new UUID
                "title": "Set up monitoring dashboard",
                "description": "Create monitoring dashboard for system health",
                "priority": "medium",
                "status": "in_progress", 
                "labels": ["monitoring", "dashboard"],
                "assignee": "",
                "due_date": "",
                "estimated_hours": 6
            }
        ]
    }
    
    # Save to a temporary file
    with open('external_tasks.json', 'w') as f:
        json.dump(external_tasks, f, indent=2)
    
    return external_tasks

def demonstrate_concatenation():
    """Demonstrate the concatenation functionality"""
    print("🔄 Task Concatenation Demo")
    print("=" * 50)
    
    # Load main TODO manager
    manager = TODOManager()
    
    # Show current tasks
    print(f"\n📋 Current tasks: {len(manager.data['tasks'])}")
    manager.print_summary()
    
    # Create and load external tasks
    print(f"\n📥 Creating external tasks...")
    external_data = create_sample_external_tasks()
    print(f"   Created {len(external_data['tasks'])} external tasks")
    
    # Concatenate the tasks
    print(f"\n🔗 Concatenating external tasks...")
    manager.concatenate_tasks(external_data)
    
    # Show updated summary
    print(f"\n📋 After concatenation:")
    manager.print_summary()
    
    print(f"\n📝 All tasks:")
    tasks = manager.list_tasks()
    for task in tasks:
        status_emoji = {"todo": "📝", "in_progress": "🔄", "done": "✅", "blocked": "🚫"}
        priority_emoji = {"low": "🔵", "medium": "🟡", "high": "🔴"}
        print(f"   {status_emoji.get(task['status'], '❓')} {priority_emoji.get(task['priority'], '⚪')} {task['title']}")
    
    # Clean up
    import os
    if os.path.exists('external_tasks.json'):
        os.remove('external_tasks.json')
    
    print(f"\n✅ Concatenation demo completed!")

if __name__ == "__main__":
    demonstrate_concatenation()