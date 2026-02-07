---
description: Today's Task Overview and Intelligent Planning
agent: jarvis
---

## System Context

Current Time: !`date "+%Y-%m-%d %H:%M %A"`

Check `just` installation: !`which just`

Check `jq` installation: !`which jq`

## Today's Tasks

!`just today`

## Overdue Tasks

!`just overdue`

## Long-term Tasks (Project Milestones)

!`just milestones`

Based on the provided data and user input, complete the following:

1. Present today's tasks in a table (time, title, notes).
2. Review the "Overdue Tasks" section and start a natural conversation with the user to help them resolve these items. Ask open-ended questions like "I see a few things from yesterday still pending like [Task]. Should we mark those as done or push them to later?"
3. Based on the user's natural language response, identify and execute the appropriate `just` commands:
   - If they say they finished it: use `just complete-task <id>` (which will also handle subtasks).
   - If they want to postpone: use `just postpone-task <id> <date>`.
   - If they want to remove it: use `just delete-task <id>`.
4. If the user has a specific question (e.g., "Am I free this afternoon?"), answer directly.
5. If there is no specific question, provide suggestions for today's schedule.

---

**Tool Tips**:

- Run `just --list` or `just help` to see all available operations.
- For unconventional queries, you can write manual `jq` (refer to `just schema`), but prioritize `just` commands.

---

## User Input

$ARGUMENTS
