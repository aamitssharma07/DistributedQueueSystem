# Distributed Task Queue System

The Distributed Task Queue System is a project aimed at efficiently distributing tasks among multiple worker nodes for parallel processing.

## Overview

This system consists of two main components:

**Queue Manager**: Responsible for managing the task queue and assigning tasks to available worker nodes.

**Worker Nodes**: Responsible for fetching tasks from the queue, processing them, and updating task completion status.

## Components

### Queue Manager (queue_manager.py)

The Queue Manager is responsible for the following tasks:

- Managing the task queue stored in `tasks_queue.json`.
- Monitoring the status of worker nodes.
- Assigning tasks to available worker nodes based on their status.
- Logging task assignment and errors in `queue_manager.log`.

### Worker Node (worker.py)

The Worker Node is responsible for the following tasks:

- Fetching tasks from the worker-specific task file (e.g., `worker-1_tasks.json`).
- Processing tasks and updating task completion status.
- Updating the worker's alive status in the centralized status file (`worker_status.json`).
- Logging task processing and errors in `workers.log`.

### GUI (Graphical User Interface)

The GUI provides a user-friendly interface to interact with the task queue system. It allows users to:

- View the status of worker nodes.
- Add new tasks to the queue.
- Monitor task processing and completion status.

The GUI is built using [insert GUI framework/library here], and the main script for the GUI is `gui.py`.

## Usage

### Queue Manager

To start the Queue Manager, run the following command:

````bash
python queue_manager.py
```
## Worker Node

To start a Worker Node, run the following command with the worker ID as an argument:

python worker.py <worker_id>
Replace <worker_id> with the ID of the worker node (e.g., 1, 2, 3).

GUI
To start the GUI, run the following command:

python gui.py

Dependencies
This project requires Python 3.x to run along with libraries tkinter
`
```
````
