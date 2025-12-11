import requests

BASE_URL = 'http://localhost:5000'

# First, let's see what tasks exist
print("Current tasks:")
response = requests.get(f'{BASE_URL}/tasks')
print(response.json())
print()

# Add a new task
print("Adding a task...")
response = requests.post(
    f'{BASE_URL}/home/tasks/add_Tasks',
    json={'description': 'Task to keep'}
)
print(response.json())
print()

# Add another task
print("Adding another task...")
response = requests.post(
    f'{BASE_URL}/home/tasks/add_Tasks',
    json={'description': 'Task to delete'}
)
task_to_delete = response.json()['task']['id']
print(response.json())
print()

# Check all tasks
print("All tasks before delete:")
response = requests.get(f'{BASE_URL}/tasks')
print(response.json())
print()

# Delete the second task
print(f"Deleting task with ID {task_to_delete}...")
response = requests.delete(
    f'{BASE_URL}/home/tasks/delete_task',
    json={'id': task_to_delete}
)
print(response.json())
print()

# Check remaining tasks
print("Remaining tasks after delete:")
response = requests.get(f'{BASE_URL}/tasks')
print(response.json())