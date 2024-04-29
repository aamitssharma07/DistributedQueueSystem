import json
import os

# File paths
queue_file_path = "tasks_queue.json"
completed_file_path = "task_completed.json"

def load_data(file_path):
    """Load data from a specified JSON file."""
    if not os.path.exists(file_path):
        if file_path == completed_file_path:
            return {}  # For completed tasks, use an empty dictionary
        return {"count": 0, "new": []}  # Properly initialize the queue file
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(data, file_path):
    """Save data to a specified JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def ensure_initial_structure(data):
    """Ensure the initial structure of the data includes 'count' and 'new' keys."""
    if 'count' not in data:
        data['count'] = 0
    if 'new' not in data:
        data['new'] = []

def enqueue_new(task_id, description):
    """Add a new task to the queue."""
    if not task_id or not description:
        return "Task ID and description cannot be empty."

    data = load_data(queue_file_path)
    ensure_initial_structure(data)  # Ensure data structure is correct
    data["new"].append({"id": task_id, "description": description})
    data["count"] += 1
    save_data(data, queue_file_path)
    return "Task added successfully."

def dequeue_completed():
    """Fetch a completed task from the completed tasks file and remove it."""
    data = load_data(completed_file_path)
    if not data:
        return None, "No completed tasks to fetch."

    # Get the first completed task and its result
    if data:
        task_id, result = next(iter(data.items()))
        del data[task_id]  # Remove the task from the dictionary
        save_data(data, completed_file_path)
        return task_id, result
    else:
        return None, "No completed tasks to fetch."


def get_count():
    """Return the count of tasks submitted."""
    data = load_data(queue_file_path)
    return data["count"]

if __name__ == "__main__":
    # Example operations for demonstration
    print(enqueue_new("task1", "Process data for analysis"))
    print(enqueue_new("task2", "Generate report from dataset"))
    print("Total tasks submitted:", get_count())
    # Example of dequeueing a completed task
    print(dequeue_completed())
