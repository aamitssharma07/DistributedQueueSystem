import tkinter as tk
from tkinter import ttk
from file_queue import enqueue_new, dequeue_completed, get_count

# Global counters for the GUI
submitted_count = 0
completed_count = 0

def submit_task():
    global submitted_count
    task_id = task_id_entry.get().strip()
    task_description = task_description_entry.get().strip()
    if task_id and task_description:  # Validate that the task ID and description are not empty
        enqueue_new(task_id, task_description)
        submitted_count += 1  # Increment the submitted task count
        task_id_entry.delete(0, tk.END)
        task_description_entry.delete(0, tk.END)
        update_status()
        print(f"Debug: Submitted task '{task_id}': '{task_description}'. Total submitted: {submitted_count}")
    else:
        status_label.config(text="Please enter both task ID and description before submitting.")

def fetch_task():
    global completed_count
    task_id, message = dequeue_completed()
    update_status()
    if task_id:
        completed_count += 1  # Increment the completed task count
        status_label.config(text=f"Fetched task: {task_id} with result {message}")
        print(f"Debug: Fetched completed task '{task_id}'. Total completed: {completed_count}")
    else:
        status_label.config(text=message)

def update_status():
    # Use the global counters to update the status label
    status_label.config(text=f"Tasks Submitted: {submitted_count}, Tasks Completed: {completed_count}")
    print(f"Debug: Updated GUI. Submitted: {submitted_count}, Completed: {completed_count}")

def setup_gui():
    window = tk.Tk()
    window.title("Task Management GUI")
    window.configure(background='light blue')

    # Center window on screen
    window_width = 500
    window_height = 250
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    main_frame = ttk.Frame(window, padding="10 10 10 10")
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    global task_id_entry, task_description_entry
    ttk.Label(main_frame, text="Task ID:").grid(column=0, row=0, sticky='w')
    task_id_entry = ttk.Entry(main_frame, width=20)
    task_id_entry.grid(column=1, row=0, pady=10)

    ttk.Label(main_frame, text="Description:").grid(column=0, row=1, sticky='w')
    task_description_entry = ttk.Entry(main_frame, width=50)
    task_description_entry.grid(column=1, row=1, pady=10)

    submit_button = ttk.Button(main_frame, text="Submit Task", command=submit_task)
    submit_button.grid(column=0, row=2, pady=10)

    fetch_button = ttk.Button(main_frame, text="Fetch Task", command=fetch_task)
    fetch_button.grid(column=1, row=2, pady=10)

    global status_label
    status_label = ttk.Label(main_frame, text="")
    status_label.grid(column=0, row=3, columnspan=2, pady=10)

    style = ttk.Style()
    style.configure('TButton', background='light green', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12))
    style.configure('TLabel', background='light blue', font=('Helvetica', 12, 'bold'))

    update_status()  # Initial status update

    return window  # Ensure that the window object is returned

if __name__ == "__main__":
    gui = setup_gui()
    gui.mainloop()
