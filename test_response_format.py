# Test script to check the API response format
import json

# Simulate what the backend returns for the /api/tasks endpoint
mock_tasks_response = [
    {
        "id": "ec3be38c-fcd6-4163-be61-8fbbd8a3519f",
        "title": "Grocerry",
        "description": None,
        "status": "pending",
        "priority": "medium",
        "created_at": "2026-02-13T15:28:45.123456",
        "updated_at": "2026-02-13T15:28:45.123456",
        "completed_at": None
    },
    {
        "id": "cc0b805c-28c1-4054-a9d7-768d85d16a5c",
        "title": "Bul",
        "description": None,
        "status": "pending",
        "priority": "medium",
        "created_at": "2026-02-13T15:28:46.123456",
        "updated_at": "2026-02-13T15:28:46.123456",
        "completed_at": None
    }
]

print("Backend API response (direct array):")
print(json.dumps(mock_tasks_response, indent=2))

print("\n" + "="*50)
print("Frontend code BEFORE fix:")
print("tasksResponse =", "/* response from API */")
print("Array.isArray(tasksResponse.data) ->", "FALSE", "(because tasksResponse is the array, not an object with 'data' property)")
print("So setTasks([]) would be called -> Empty task list!")

print("\n" + "="*50)
print("Frontend code AFTER fix:")
print("tasksResponse =", "/* response from API */")
print("Array.isArray(tasksResponse) ->", "TRUE", "(because tasksResponse is the array itself)")
print("So setTasks(tasksResponse) would be called -> Tasks displayed correctly!")