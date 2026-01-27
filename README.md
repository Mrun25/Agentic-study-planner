# Agentic Study Planner

A memory-driven, multi-agent study planning system that converts long-term goals into daily tasks, syncs with Google Calendar, and autonomously adapts based on your behavior.

## Features

- **🎯 Goal Structuring**: Convert study goals into actionable plans
- **📅 Daily Planning**: Automatic generation of phase-appropriate tasks
- **📆 Calendar Sync**: Auto-add tasks to Google Calendar with reminders
- **📊 Progress Tracking**: Log completions and collect feedback
- **🔄 Adaptive Replanning**: Autonomously adjust plans based on performance

## Architecture

3-Layer design following `AGENT.md`:
- **Layer 1 (Directives)**: SOPs in `directives/` define agent workflows
- **Layer 2 (Orchestration)**: `main.py` routes to appropriate agents
- **Layer 3 (Execution)**: Python scripts in `execution/` handle deterministic operations

## Setup

1. **Install dependencies**:
   ```powershell
   pip install -r execution/requirements.txt
   ```

2. **Configure Google Calendar API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google Calendar API
   - Download OAuth credentials as `credentials.json`
   - Place in project root

3. **Configure environment**:
   - Update `.env` with your timezone (default: Asia/Kolkata)

## Usage

Run the main orchestrator:
```powershell
python main.py
```

### Workflow

1. **Create Goal** - Define study domain, target, duration
2. **Generate Plans** - System creates daily tasks and syncs to calendar
3. **Log Progress** - Track what you completed and why you didn't complete tasks
4. **Auto-Adapt** - System adjusts future plans based on your patterns

## Memory Structure

All data stored in `.tmp/memory/`:
- `goals/` - Structured goal definitions
- `plans/` - Daily task plans with calendar event IDs
- `progress/` - Completion logs and feedback
- `replanning/` - Adaptation decisions

## Multi-Agent System

### 1. Goal Agent
- **Directive**: `directives/goal_agent.md`
- **Script**: `execution/goal_structurer.py`
- **Purpose**: Structure raw goals into JSON format

### 2. Planning Agent
- **Directive**: `directives/planning_agent.md`
- **Script**: `execution/task_planner.py`
- **Purpose**: Generate daily tasks and sync to calendar

### 3. Progress Agent
- **Directive**: `directives/progress_agent.md`
- **Script**: `execution/progress_tracker.py`
- **Purpose**: Track completion and identify patterns

### 4. Replanning Agent
- **Directive**: `directives/replanning_agent.md`
- **Script**: `execution/replanner.py`
- **Purpose**: Adapt future plans based on behavior

## Example

```
🎯 Goal: Learn Python in 30 days, 2 hrs/day
📅 Days 1-10: Foundation phase (concepts + exercises)
📅 Days 11-21: Building phase (projects + advanced topics)
📅 Days 22-30: Mastery phase (final projects + documentation)

📊 After 5 days: 40% completion detected
🔄 System adapts: Reduces task complexity for next 7 days
```
