"""
Test Google Calendar Authentication and Create Sample Event
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from execution.calendar_manager import create_event, authenticate

print("🔐 Testing Google Calendar Authentication...\n")

try:
    # Authenticate (will open browser on first run)
    print("Step 1: Authenticating with Google...")
    creds = authenticate()
    print("✅ Authentication successful!\n")
    
    # Create a test event
    print("Step 2: Creating test calendar event...\n")
    
    test_time = datetime.now() + timedelta(hours=1)
    
    event_id = create_event(
        summary="🎯 Test Event - Study Planner",
        description="This is a test event from your Agentic Study Planner.\nIf you see this in your calendar, the integration is working!",
        start_time=test_time,
        duration_minutes=30,
        reminder_minutes=10
    )
    
    print(f"✅ Test event created successfully!")
    print(f"   Event ID: {event_id}")
    print(f"   Time: {test_time.strftime('%Y-%m-%d %I:%M %p')}")
    print(f"   Duration: 30 minutes")
    print(f"\n📅 Check your Google Calendar - you should see:")
    print(f"   '🎯 Test Event - Study Planner'")
    print(f"   Scheduled for: {test_time.strftime('%I:%M %p today')}")
    
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("\n💡 Make sure credentials.json is in the project folder")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 If you see an authentication error:")
    print("   1. A browser should have opened")
    print("   2. Sign in to your Google account")
    print("   3. Click 'Allow' to grant calendar access")
    
    import traceback
    traceback.print_exc()
