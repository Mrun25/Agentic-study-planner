"""
Main Orchestrator - CLI interface for the Agentic Study Planner.
Entry point for all user interactions.
"""

import sys
from datetime import datetime, date, timedelta
from pathlib import Path

# Add execution directory to path
sys.path.append(str(Path(__file__).parent / 'execution'))

from execution import (
    memory_manager,
    goal_structurer,
    task_planner,
    progress_tracker,
    replanner
)


def display_menu():
    """Display main menu."""
    print("\n" + "="*50)
    print("  AGENTIC STUDY PLANNER")
    print("="*50)
    print("\n1. Create New Goal")
    print("2. View Active Goals")
    print("3. Create Daily Plan")
    print("4. Log Progress")
    print("5. View Insights")
    print("6. Trigger Replanning")
    print("7. Exit")
    print("-"*50)


def create_goal_workflow():
    """Workflow for creating a new goal (Goal Agent)."""
    print("\n🎯 GOAL AGENT - Create New Study Goal")
    print("Following directive: directives/goal_agent.md\n")
    
    try:
        goal_data = goal_structurer.create_goal_interactive()
        memory_manager.save_goal(goal_data)
        
        print(f"\n✅ Goal created successfully!")
        print(f"   Goal ID: {goal_data['goal_id']}")
        print(f"   Domain: {goal_data['domain']}")
        print(f"   Target: {goal_data['target_outcome']}")
        print(f"   Duration: {goal_data['duration_days']} days")
        print(f"   Daily Hours: {goal_data['daily_hours']}")
        print(f"   Start Date: {goal_data['start_date']}")
        
        # Offer to create first day plan
        create_plan = input("\nCreate plan for today? (y/n): ").lower().strip()
        if create_plan == 'y':
            create_daily_plan_workflow(goal_data['goal_id'])
    
    except Exception as e:
        print(f"\n❌ Error creating goal: {e}")


def view_goals_workflow():
    """Display all active goals."""
    print("\n📋 ACTIVE GOALS\n")
    
    goals = memory_manager.get_goals(active_only=True)
    
    if not goals:
        print("No active goals found.")
        print("Create a goal from the main menu!")
        return
    
    for i, goal in enumerate(goals, 1):
        print(f"{i}. [{goal['goal_id']}] {goal['domain']}")
        print(f"   Target: {goal['target_outcome']}")
        print(f"   Duration: {goal['duration_days']} days | Daily: {goal['daily_hours']} hrs")
        print(f"   Started: {goal['start_date']}")
        
        # Show quick stats
        stats = memory_manager.get_progress_stats(goal['goal_id'])
        if stats['total_days'] > 0:
            print(f"   Progress: {stats['total_days']} days logged | Avg: {stats['avg_completion_rate']*100:.0f}%")
        print()


def create_daily_plan_workflow(goal_id: str = None):
    """Workflow for creating daily plan (Planning Agent)."""
    print("\n📅 PLANNING AGENT - Create Daily Plan")
    print("Following directive: directives/planning_agent.md\n")
    
    if not goal_id:
        goals = memory_manager.get_goals(active_only=True)
        if not goals:
            print("No active goals. Create a goal first!")
            return
        
        print("Select goal:")
        for i, goal in enumerate(goals, 1):
            print(f"{i}. {goal['domain']} - {goal['target_outcome']}")
        
        choice = input("\nGoal number: ").strip()
        try:
            goal_id = goals[int(choice) - 1]['goal_id']
        except (ValueError, IndexError):
            print("Invalid selection")
            return
    
    # Get date
    date_input = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    target_date = date_input if date_input else date.today().strftime('%Y-%m-%d')
    
    # Get start time
    time_input = input("Start time (HH:MM, press Enter for 09:00): ").strip()
    start_time = time_input if time_input else "09:00"
    
    try:
        print("\n⏳ Generating plan and syncing to Google Calendar...")
        plan = task_planner.create_daily_plan(goal_id, target_date, start_time)
        
        print(f"\n✅ Plan created for {target_date}!")
        print(f"   Day {plan['day_number']} of study plan")
        print(f"   Total duration: {plan['total_duration_minutes']} minutes")
        print(f"\n📋 Tasks:")
        
        for i, task in enumerate(plan['tasks'], 1):
            status = "📅" if task.get('calendar_event_id') else "⚠️"
            print(f"   {status} {i}. {task['title']}")
            print(f"      {task['duration_minutes']} min | Priority: {task['priority']}")
        
        print("\n✅ Calendar events created with 30-min reminders!")
    
    except Exception as e:
        print(f"\n❌ Error creating plan: {e}")


def log_progress_workflow():
    """Workflow for logging progress (Progress Agent)."""
    print("\n📊 PROGRESS AGENT - Log Daily Progress")
    print("Following directive: directives/progress_agent.md\n")
    
    goals = memory_manager.get_goals(active_only=True)
    if not goals:
        print("No active goals. Create a goal first!")
        return
    
    print("Select goal:")
    for i, goal in enumerate(goals, 1):
        print(f"{i}. {goal['domain']} - {goal['target_outcome']}")
    
    choice = input("\nGoal number: ").strip()
    try:
        goal_id = goals[int(choice) - 1]['goal_id']
    except (ValueError, IndexError):
        print("Invalid selection")
        return
    
    date_input = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    target_date = date_input if date_input else date.today().strftime('%Y-%m-%d')
    
    try:
        progress_tracker.log_progress_interactive(goal_id, target_date)
    except Exception as e:
        print(f"\n❌ Error logging progress: {e}")


def view_insights_workflow():
    """Display insights for a goal."""
    print("\n📈 INSIGHTS\n")
    
    goals = memory_manager.get_goals(active_only=True)
    if not goals:
        print("No active goals.")
        return
    
    print("Select goal:")
    for i, goal in enumerate(goals, 1):
        print(f"{i}. {goal['domain']} - {goal['target_outcome']}")
    
    choice = input("\nGoal number: ").strip()
    try:
        goal_id = goals[int(choice) - 1]['goal_id']
    except (ValueError, IndexError):
        print("Invalid selection")
        return
    
    insights = progress_tracker.get_insights(goal_id)
    print(f"\n{insights}")


def trigger_replanning_workflow():
    """Workflow for adaptive replanning (Replanning Agent)."""
    print("\n🔄 REPLANNING AGENT - Adaptive Plan Adjustment")
    print("Following directive: directives/replanning_agent.md\n")
    
    goals = memory_manager.get_goals(active_only=True)
    if not goals:
        print("No active goals.")
        return
    
    print("Select goal:")
    for i, goal in enumerate(goals, 1):
        print(f"{i}. {goal['domain']} - {goal['target_outcome']}")
    
    choice = input("\nGoal number: ").strip()
    try:
        goal_id = goals[int(choice) - 1]['goal_id']
    except (ValueError, IndexError):
        print("Invalid selection")
        return
    
    try:
        replanner.trigger_replanning_interactive(goal_id)
    except Exception as e:
        print(f"\n❌ Error during replanning: {e}")


def main():
    """Main orchestrator loop."""
    print("\n🚀 Welcome to Agentic Study Planner")
    print("A memory-driven, multi-agent study planning system")
    
    while True:
        display_menu()
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            create_goal_workflow()
        elif choice == '2':
            view_goals_workflow()
        elif choice == '3':
            create_daily_plan_workflow()
        elif choice == '4':
            log_progress_workflow()
        elif choice == '5':
            view_insights_workflow()
        elif choice == '6':
            trigger_replanning_workflow()
        elif choice == '7':
            print("\n👋 Goodbye! Keep learning!\n")
            break
        else:
            print("\n❌ Invalid option. Please select 1-7.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
        sys.exit(0)
