import json
import time
import logging
import sys
from threading import Lock

# Read worker ID from command line arguments
worker_id = sys.argv[1] if len(sys.argv) > 1 else '1'

# Setup centralized logging
logging.basicConfig(filename='workers.log', level=logging.INFO,
                    format=f'%(asctime)s:Worker-{worker_id}:%(levelname)s:%(message)s')

worker_file = f'worker-{worker_id}_tasks.json'
task_completed_file = 'task_completed.json'  # New JSON file for storing completed task results
lock = Lock()

def process_task(task):
    character_count = len(task['description'])
    logging.info(f"Processed task: {task['id']} - {task['description']}. Character count: {character_count}")
    time.sleep(2)  # Simulate processing time
    return task['id'], character_count

def update_completed_tasks(task_id, count):
    with lock:
        try:
            with open(task_completed_file, 'r+') as file:
                completed_data = json.load(file)
                completed_data[task_id] = count  # Store task ID as key and count as value
                file.seek(0)
                json.dump(completed_data, file)
                file.truncate()
                logging.info(f"Task {task_id} result stored in {task_completed_file}")
        except FileNotFoundError:
            # Create a new file if it doesn't exist
            with open(task_completed_file, 'w') as file:
                json.dump({task_id: count}, file)
                logging.info(f"Created new file {task_completed_file} and stored task {task_id} result.")
        except Exception as e:
            logging.error(f"Failed to update completed tasks: {e}")

def fetch_and_process_tasks():
    while True:
        try:
            with open(worker_file, 'r+') as file:
                tasks = json.load(file)
                if tasks:
                    task = tasks.pop(0)
                    file.seek(0)
                    json.dump(tasks, file)
                    file.truncate()
                    logging.info(f"Task {task['id']} fetched for processing.")
                    task_id, character_count = process_task(task)
                    update_completed_tasks(task_id, character_count)
                else:
                    logging.info(f"No tasks available for Worker-{worker_id}. Waiting for new tasks.")
                    time.sleep(5)  # Sleep longer if no tasks are available
        except FileNotFoundError:
            logging.error(f"Worker file {worker_file} not found.")
            time.sleep(10)  # Wait longer before retrying
        except json.JSONDecodeError:
            logging.error(f"JSON decode error in file {worker_file}.")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    logging.info(f"Worker {worker_id} started.")
    fetch_and_process_tasks()
