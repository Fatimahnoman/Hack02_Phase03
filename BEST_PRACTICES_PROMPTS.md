# OpenRouter AI Chatbot - Best Practices for Task Creation with Date Information

## Current Status
✅ OpenRouter API integration is working correctly
✅ Custom success messages are displayed ("Yes! I've successfully added your task to the task manager 🌟")
✅ Tasks are properly saved to the database
✅ All CRUD operations are functional

## Issue Identified
The AI model sometimes interprets date information as part of the task title rather than as scheduling information. For example:
- Input: "add task name operation on 23 feb 2026"
- Result: Title="Operation on 23 Feb 2026" instead of Title="Operation" with date in description

## Recommended Prompts for Better Date/Task Separation

### Format 1: Explicit Title/Description Structure
- "Create a task with title 'Operation' and description 'Heart surgery on 23 Feb 2026'"
- "Add a task titled 'Meeting' about 'Team sync scheduled for 15 Mar 2026'"
- "Make a task called 'Review' for '20 Mar 2026' with details 'Code review with team'"

### Format 2: Structured Task Creation
- "New task: Title=Operation, Date=23 Feb 2026, Description=Heart surgery"
- "Task: Title=Appointment, Date=15 Jan 2026, Description=Dental checkup"
- "Create task: Name=Presentation, Date=10 Apr 2026, Info=Quarterly review"

### Format 3: Action-Based Phrasing
- "Schedule Operation for 23 Feb 2026 with details Heart surgery"
- "Plan Meeting on 15 Mar 2026 about Team synchronization"
- "Set up Appointment at 20 Jan 2026 for Dental checkup"

### Format 4: Clear Separation Keywords
- "Create [TASK_NAME] task for [DATE] with description [DESCRIPTION]"
- "Add [TASK_NAME] scheduled on [DATE] - [DESCRIPTION]"
- "Make [TASK_NAME] event for [DATE]: [DESCRIPTION]"

## Why This Happens
The AI model processes natural language and sometimes treats phrases like "operation on 23 feb" as a single entity. Using more explicit language helps the AI understand the structure you want.

## Implementation Notes
The backend is correctly configured to:
1. Accept task creation requests via the chat interface
2. Parse date information from titles and move to descriptions when detected
3. Return custom success messages with emojis
4. Save tasks to the database properly

## Troubleshooting Tips
- If dates appear in titles, try using more explicit prompts with "Title=" and "Description=" keywords
- Use structured language that clearly separates the task name from the date
- Consider using standard date formats (DD MMM YYYY) for better recognition
- If needed, you can manually edit tasks after creation through the API or UI

## Example Successful Requests
- "Create a task with title 'Doctor Visit' and description 'Annual checkup on 15 June 2026'"
- "Add meeting scheduled for 20 July 2026 with title 'Team Sync' and description 'Weekly team meeting'"
- "Make appointment called 'Dentist' for '10 August 2026' with details 'Regular cleaning'"