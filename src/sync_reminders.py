import json
import subprocess
import sys
from pathlib import Path
from typing import List

from pydantic import TypeAdapter

from src.models.task import Task

TASKS_FILE = Path("data/tasks.json")
LIST_NAME = "Jarvis"


def run_applescript(script: str):
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running AppleScript: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout.strip()


def sync_task_to_reminder(task: Task):
    # Prepare dates for AppleScript
    due_date_str = ""
    if task.due_at:
        due_date_str = task.due_at.strftime("%Y-%m-%d %H:%M:%S")

    completed = "true" if task.status == "done" else "false"

    # AppleScript to find or create/update
    script = f'''
    tell application "Reminders"
        if not (exists list "{LIST_NAME}") then
            make new list with properties {{name:"{LIST_NAME}"}}
        end if
        set jarvisList to list "{LIST_NAME}"

        set existingReminders to (reminders of jarvisList whose body contains "{task.id}")
        if (count of existingReminders) > 0 then
            set theReminder to item 1 of existingReminders
            set name of theReminder to "{task.title}"
            set completed of theReminder to {completed}
            '''
    if task.due_at:
        script += f'set remind me date of theReminder to (date "{due_date_str}")\n'
    else:
        script += """
            try
                set remind me date of theReminder to missing value
            end try
        """

    script += f'''
        else
            set props to {{name:"{task.title}", body:"{task.id}", completed:{completed}}}
            set newRem to make new reminder at jarvisList with properties props
            '''
    if task.due_at:
        script += f'set remind me date of newRem to (date "{due_date_str}")\n'

    script += """
        end if
    end tell
    """
    run_applescript(script)


def main():
    if not TASKS_FILE.exists():
        print(f"Tasks file not found: {TASKS_FILE}")
        return

    with open(TASKS_FILE, "r") as f:
        data = json.load(f)

    adapter = TypeAdapter(List[Task])
    tasks = adapter.validate_python(data)

    print(f"Syncing {len(tasks)} tasks to Reminders...")
    for task in tasks:
        if task.status != "cancelled":
            print(f"  - {task.title}")
            sync_task_to_reminder(task)
    print("Sync complete.")


if __name__ == "__main__":
    main()
