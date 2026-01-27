# Calendar Execution Agent

A standalone, terminal-based agent that schedules study tasks to Google Calendar.

## Purpose
**Execution-only**: No planning, no reasoning. Only reliable calendar scheduling.

## Usage

### From File
```powershell
python calendar_agent.py < tasks.json
```

### From Pipe
```powershell
echo '{"date":"2026-01-28","tasks":[{"task_id":"t1","title":"Study AWS","duration_minutes":90}]}' | python calendar_agent.py
```

### From Another Program
```python
import subprocess
import json

payload = {
    "date": "2026-01-28",
    "tasks": [
        {
            "task_id": "task_1",
            "title": "Cloud Computing - Core Concepts",
            "duration_minutes": 90
        }
    ]
}

result = subprocess.run(
    ['python', 'calendar_agent.py'],
    input=json.dumps(payload),
    capture_output=True,
    text=True
)

response = json.loads(result.stdout)
print(response['events_created'])  # Number of events created
```

## Input Format

```json
{
  "date": "YYYY-MM-DD",
  "tasks": [
    {
      "task_id": "string",
      "title": "string",
      "duration_minutes": number,
      "description": "optional string"
    }
  ]
}
```

## Output Format

```json
{
  "status": "success",
  "scheduled_date": "YYYY-MM-DD",
  "total_tasks": 3,
  "events_created": 3,
  "events": [
    {
      "task_id": "cc-day2-task1",
      "event_id": "google_calendar_event_id",
      "start_time": "2026-01-28T09:00:00",
      "end_time": "2026-01-28T10:30:00"
    }
  ]
}
```

## Configuration

Set in `.env`:
```bash
DEFAULT_START_HOUR=9          # Start time (default 09:00)
DEFAULT_START_MINUTE=0
TASK_BUFFER_MINUTES=15        # Buffer between tasks
REMINDER_MINUTES=30           # Reminder before each task
```

## Error Handling

Exits with code 1 and outputs to stderr:
- Invalid JSON
- Missing required fields
- Calendar API failures
- Authentication errors

## Example

Test with the provided example:
```powershell
python calendar_agent.py < example_tasks.json
```

Output:
```json
{
  "status": "success",
  "scheduled_date": "2026-01-28",
  "total_tasks": 3,
  "events_created": 3,
  "events": [...]
}
```

## Integration

This agent is designed to be called by other agents or systems:
- Planning agents generate task JSON
- Pipe to this agent for calendar scheduling
- Parse output to get event IDs for tracking
