"""
Calendar Execution Agent - Terminal-based task scheduler.
Execution-only: receives structured JSON, writes to Google Calendar.
No planning, no reasoning, only scheduling.

USAGE:
  python calendar_agent.py < tasks.json
  echo '{"date":"2026-01-28","tasks":[...]}' | python calendar_agent.py
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from execution.calendar_manager import create_event, get_service
import os
from dotenv import load_dotenv

load_dotenv()


def parse_input():
    """Read JSON from stdin."""
    try:
        data = json.load(sys.stdin)
        return data
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read input: {e}", file=sys.stderr)
        sys.exit(1)


def validate_payload(data):
    """Validate input structure."""
    if not isinstance(data, dict):
        print("ERROR: Input must be a JSON object", file=sys.stderr)
        sys.exit(1)
    
    if 'date' not in data:
        print("ERROR: Missing required field 'date'", file=sys.stderr)
        sys.exit(1)
    
    if 'tasks' not in data or not isinstance(data['tasks'], list):
        print("ERROR: Missing or invalid 'tasks' array", file=sys.stderr)
        sys.exit(1)
    
    # Validate date format
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        print("ERROR: Invalid date format. Expected YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    
    # Validate each task
    for i, task in enumerate(data['tasks']):
        if not isinstance(task, dict):
            print(f"ERROR: Task {i} is not an object", file=sys.stderr)
            sys.exit(1)
        
        required = ['task_id', 'title', 'duration_minutes']
        for field in required:
            if field not in task:
                print(f"ERROR: Task {i} missing required field '{field}'", file=sys.stderr)
                sys.exit(1)
        
        if not isinstance(task['duration_minutes'], (int, float)):
            print(f"ERROR: Task {i} duration_minutes must be a number", file=sys.stderr)
            sys.exit(1)


def schedule_tasks(data):
    """
    Schedule tasks to Google Calendar.
    Returns list of created event IDs.
    """
    target_date = data['date']
    tasks = data['tasks']
    
    # Get start time from config or default to 09:00
    start_hour = int(os.getenv('DEFAULT_START_HOUR', '9'))
    start_minute = int(os.getenv('DEFAULT_START_MINUTE', '0'))
    
    # Parse date and create start time
    date_obj = datetime.strptime(target_date, '%Y-%m-%d')
    current_time = date_obj.replace(hour=start_hour, minute=start_minute)
    
    # Get buffer time between tasks (default 15 min)
    buffer_minutes = int(os.getenv('TASK_BUFFER_MINUTES', '15'))
    
    # Get reminder time (default 30 min)
    reminder_minutes = int(os.getenv('REMINDER_MINUTES', '30'))
    
    # Test calendar connection first
    try:
        service = get_service()
    except Exception as e:
        print(f"ERROR: Could not connect to Google Calendar: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Schedule each task
    event_ids = []
    for task in tasks:
        try:
            event_id = create_event(
                summary=task['title'],
                description=f"Task ID: {task['task_id']}\n{task.get('description', '')}",
                start_time=current_time,
                duration_minutes=int(task['duration_minutes']),
                reminder_minutes=reminder_minutes
            )
            
            event_ids.append({
                'task_id': task['task_id'],
                'event_id': event_id,
                'start_time': current_time.isoformat(),
                'end_time': (current_time + timedelta(minutes=task['duration_minutes'])).isoformat()
            })
            
            # Move to next time slot
            current_time += timedelta(minutes=task['duration_minutes'] + buffer_minutes)
            
        except Exception as e:
            print(f"ERROR: Failed to create event for task {task['task_id']}: {e}", file=sys.stderr)
            # Continue with other tasks
    
    return event_ids


def main():
    """Main execution flow."""
    # Read and validate input
    data = parse_input()
    validate_payload(data)
    
    # Schedule tasks
    result = schedule_tasks(data)
    
    # Output results as JSON
    output = {
        'status': 'success',
        'scheduled_date': data['date'],
        'total_tasks': len(data['tasks']),
        'events_created': len(result),
        'events': result
    }
    
    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
