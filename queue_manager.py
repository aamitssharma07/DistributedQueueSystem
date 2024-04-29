import time
import json
import logging
from threading import Lock

# Setup logging
logging.basicConfig(filename='queue_manager.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Path to the JSON queue file
queue_file = 'tasks_queue.json'
queue_lock = Lock()

# Initialize worker task files
# List of worker files to simulate a round-robin load balancing
workers = ['worker-1_tasks.json', 'worker-2_tasks.json', 'worker-3_tasks.json']
for worker in workers:
    with open(worker, 'w') as file:
        json.dump([], file)  # Write an empty list to each worker file

current_worker = 0

def dequeue_new():
    with queue_lock:
        try:
            with open(queue_file, 'r') as file:
                queue_data = json.load(file)
            tasks = queue_data.get('new', [])
            if tasks:
                task = tasks.pop(0)
                queue_data['new'] = tasks
                with open(queue_file, 'w') as file:
                    json.dump(queue_data, file)
                return task
        except Exception as e:
            logging.error(f"Failed to dequeue task: {e}")
        return None

def enqueue_new(task):
    with queue_lock:
        try:
            with open(queue_file, 'r') as file:
                queue_data = json.load(file)
            tasks = queue_data.get('new', [])
            tasks.append(task)
            queue_data['new'] = tasks
            with open(queue_file, 'w') as file:
                json.dump(queue_data, file)
            logging.debug(f"Task enqueued successfully: {task}")
        except Exception as e:
            logging.error(f"Failed to enqueue task: {e}")

def monitor_queue():
    global current_worker
    while True:
        task = dequeue_new()
        if task:
            assign_task_to_worker(task, workers[current_worker])
            current_worker = (current_worker + 1) % len(workers)
        else:
            logging.debug("No new tasks to assign, queue is empty.")
            time.sleep(1)  # Sleep for 1 second before checking again

def assign_task_to_worker(task, worker_file):
    try:
        with open(worker_file, 'r+') as file:
            worker_tasks = json.load(file)
            worker_tasks.append(task)
            file.seek(0)
            json.dump(worker_tasks, file)
        logging.info(f"Task assigned to {worker_file}: {task}")
    except Exception as e:
        logging.error(f"Failed to assign task to {worker_file}: {task} with error {e}")
        # Re-queue task in case of failure
        enqueue_new(task)

if __name__ == "__main__":
    logging.info("Queue Manager started.")
    monitor_queue()
