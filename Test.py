import requests

BASE_URL = 'http://localhost:5000'

print("=== TESTING DELETE WITH VALIDATION ===\n")

# Test 1: Add some tasks first
print("1. Adding tasks...")
for i in range(1, 4):
    response = requests.post(
        f'{BASE_URL}/home/tasks/add_Tasks',
        json={'description': f'Task {i}'}
    )
    print(f"   Added: {response.json()}")

# Test 2: View all tasks
print("\n2. Current tasks:")
response = requests.get(f'{BASE_URL}/home/tasks')
all_tasks = response.json()['tasks']
for task in all_tasks:
    print(f"   ID {task['id']}: {task['description']}")

# Test 3: Delete with valid ID
if all_tasks:
    valid_id = all_tasks[0]['id']
    print(f"\n3. Deleting task with valid ID {valid_id}:")
    response = requests.delete(
        f'{BASE_URL}/home/tasks/delete_task',
        json={'id': valid_id}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

# Test 4: Try to delete non-existent ID
print("\n4. Trying to delete non-existent ID 9999:")
response = requests.delete(
    f'{BASE_URL}/home/tasks/delete_task',
    json={'id': 9999}
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

# Test 5: Try to delete without ID
print("\n5. Trying to delete without providing ID:")
response = requests.delete(
    f'{BASE_URL}/home/tasks/delete_task',
    json={'description': 'something'}  # Wrong field, no 'id'
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

# Test 6: Try to delete with no data at all
print("\n6. Trying to delete with no JSON data:")
response = requests.delete(
    f'{BASE_URL}/home/tasks/delete_task'
    # No json parameter at all
)
print(f"   Status: {response.status_code}")
#print(f"   Response: {response.json()}")

# Test 7: Final state
print("\n7. Final remaining tasks:")
response = requests.get(f'{BASE_URL}/home/tasks')
remaining = response.json()['tasks']
if remaining:
    for task in remaining:
        print(f"   ID {task['id']}: {task['description']}")
else:
    print("   No tasks remaining")

print("\n=== ALL TESTS COMPLETE ===")