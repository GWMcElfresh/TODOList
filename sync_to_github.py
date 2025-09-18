#!/usr/bin/env python3
"""
GitHub Project Board Synchronization Script
Syncs TODO list items to GitHub Issues for project board integration
"""

import json
import os
import requests
import sys
from typing import Dict, List, Any, Optional

class GitHubSync:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo = os.getenv('GITHUB_REPOSITORY')
        
        if not self.token or not self.repo:
            raise ValueError("GITHUB_TOKEN and GITHUB_REPOSITORY environment variables must be set")
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        self.base_url = f'https://api.github.com/repos/{self.repo}'
    
    def get_existing_issues(self) -> Dict[str, Dict]:
        """Get existing issues that were created from TODO items"""
        url = f'{self.base_url}/issues'
        params = {
            'labels': 'todo-list-item',
            'state': 'all',
            'per_page': 100
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            print(f"Warning: Could not fetch existing issues: {response.status_code}")
            return {}
        
        issues = {}
        for issue in response.json():
            # Extract TODO ID from issue body
            body = issue.get('body', '')
            if '<!-- TODO-ID:' in body:
                todo_id = body.split('<!-- TODO-ID:')[1].split('-->')[0].strip()
                issues[todo_id] = issue
        
        return issues
    
    def create_or_update_issue(self, task: Dict[str, Any], existing_issue: Optional[Dict] = None) -> bool:
        """Create a new issue or update existing one for a TODO task"""
        # Map TODO status to GitHub issue state
        status_map = {
            'todo': 'open',
            'in_progress': 'open',
            'done': 'closed',
            'blocked': 'open'
        }
        
        # Map priority to labels
        priority_labels = {
            'low': 'priority: low',
            'medium': 'priority: medium', 
            'high': 'priority: high'
        }
        
        # Prepare labels
        labels = ['todo-list-item']
        if task.get('priority'):
            labels.append(priority_labels.get(task['priority'], 'priority: medium'))
        
        if task.get('status') == 'blocked':
            labels.append('blocked')
        elif task.get('status') == 'in_progress':
            labels.append('in progress')
        
        # Add custom labels from task
        if task.get('labels'):
            labels.extend(task['labels'])
        
        # Prepare issue body
        body_parts = []
        if task.get('description'):
            body_parts.append(task['description'])
        
        # Add metadata
        body_parts.append('\n---\n**TODO List Item Details:**')
        body_parts.append(f'- **Priority:** {task.get("priority", "medium")}')
        body_parts.append(f'- **Status:** {task.get("status", "todo")}')
        if task.get('assignee'):
            body_parts.append(f'- **Assignee:** {task["assignee"]}')
        if task.get('due_date'):
            body_parts.append(f'- **Due Date:** {task["due_date"]}')
        if task.get('estimated_hours'):
            body_parts.append(f'- **Estimated Hours:** {task["estimated_hours"]}')
        
        body_parts.append(f'\n<!-- TODO-ID: {task["id"]} -->')
        
        issue_data = {
            'title': task['title'],
            'body': '\n'.join(body_parts),
            'labels': labels,
            'state': status_map.get(task.get('status'), 'open')
        }
        
        # Assign if assignee is provided
        if task.get('assignee'):
            issue_data['assignees'] = [task['assignee']]
        
        try:
            if existing_issue:
                # Update existing issue
                url = f"{self.base_url}/issues/{existing_issue['number']}"
                response = requests.patch(url, headers=self.headers, json=issue_data)
                action = "Updated"
            else:
                # Create new issue
                url = f'{self.base_url}/issues'
                response = requests.post(url, headers=self.headers, json=issue_data)
                action = "Created"
            
            if response.status_code in [200, 201]:
                issue_number = response.json()['number']
                print(f"✅ {action} issue #{issue_number}: {task['title']}")
                return True
            else:
                print(f"❌ Failed to {action.lower()} issue for task '{task['title']}': {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ Error processing task '{task['title']}': {e}")
            return False
    
    def sync_todo_list(self, todo_file: str = 'todo_list.json') -> None:
        """Sync entire TODO list to GitHub issues"""
        if not os.path.exists(todo_file):
            print(f"❌ TODO file '{todo_file}' not found")
            return
        
        # Load TODO data
        try:
            with open(todo_file, 'r', encoding='utf-8') as f:
                todo_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error reading TODO file: {e}")
            return
        
        tasks = todo_data.get('tasks', [])
        if not tasks:
            print("ℹ️ No tasks found in TODO list")
            return
        
        print(f"🔄 Syncing {len(tasks)} tasks to GitHub issues...")
        
        # Get existing issues
        existing_issues = self.get_existing_issues()
        
        # Process each task
        success_count = 0
        for task in tasks:
            task_id = task.get('id')
            if not task_id:
                print(f"⚠️ Skipping task without ID: {task.get('title', 'Unknown')}")
                continue
            
            existing_issue = existing_issues.get(task_id)
            if self.create_or_update_issue(task, existing_issue):
                success_count += 1
        
        print(f"\n📊 Sync completed: {success_count}/{len(tasks)} tasks processed successfully")
        
        # Generate summary
        summary = todo_data.get('metadata', {})
        print(f"\n📋 TODO List Summary:")
        print(f"   Total tasks: {summary.get('total_tasks', len(tasks))}")
        print(f"   Completed: {summary.get('completed_tasks', 0)}")
        print(f"   Last updated: {summary.get('last_updated', 'Unknown')}")

def main():
    """Main function"""
    try:
        syncer = GitHubSync()
        syncer.sync_todo_list()
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()