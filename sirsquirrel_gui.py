import tkinter as tk
from tkinter import messagebox
import threading
import time
from src import core, mirror, mirror_utils  # Assuming these are valid imports

# Global stop flag to interrupt the running process
stop_flag = False

# Load the status from the file
with open("config/status_selection.txt", "r") as f:
    status = [i.strip().lower() for i in f.readlines()]

# Function to handle the long-running process
def wuthering_run(num_runs):
    global stop_flag
    run_count = 0
    win_count = 0
    lose_count = 0

    status_list = (status * ((num_runs // len(status)) + 1))[:num_runs]
    
    print("Starting Run")
    for i in range(num_runs):
        if stop_flag:  # Check if the process should stop
            print("Run interrupted!")
            break
        print("Run {}".format(run_count + 1))
        #time.sleep(1)  # Simulate a long-running task (e.g., waiting for battle results)
        #core.refill_enkephalin()
        #core.navigate_to_md()
        squad_order = mirror.set_sinner_order(status_list[i])
        run_complete = 0
        win_flag = 0
        while run_complete != 1 and not stop_flag:
            win_flag, run_complete = mirror.start_mirror(status_list[i], squad_order)

        if win_flag == 1:
            win_count += 1
        else:
            lose_count += 1
        run_count += 1

    result_message = f"Won Runs: {win_count}, Lost Runs: {lose_count}"
    print(result_message)
    
    # Show results in a messagebox after the run completes
    if not stop_flag:
        messagebox.showinfo("Result", result_message)
    else:
        messagebox.showinfo("Result", "Run was interrupted!")

# Function to start the process in a separate thread
def start_run():
    global stop_flag
    stop_flag = False  # Reset the stop flag
    
    try:
        num_runs = int(entry.get())  # Get the number of runs from input
        thread = threading.Thread(target=wuthering_run, args=(num_runs,))
        thread.start()  # Run the wuthering_run function in a separate thread
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer.")

# Function to stop the running process
def stop_run():
    global stop_flag
    stop_flag = True  # Set the stop flag to interrupt the process

# Function to handle window close event
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Safely close the window

# Create the GUI window
root = tk.Tk()
root.title("Wuthering Run Bot")

# Set window size and disable resizing
root.geometry("400x250")
root.resizable(False, False)

# Bind window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a frame for the content
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

# Add a label for input
label = tk.Label(frame, text="Enter number of runs:", font=("Helvetica", 12))
label.grid(row=0, column=0, pady=10)

# Add an entry widget for user input
entry = tk.Entry(frame, width=10, font=("Helvetica", 12))
entry.grid(row=0, column=1, pady=10)

# Create a start button
start_button = tk.Button(frame, text="Start", font=("Helvetica", 12), command=start_run, width=10)
start_button.grid(row=1, column=0, pady=20)

# Create a stop button
stop_button = tk.Button(frame, text="Stop", font=("Helvetica", 12), command=stop_run, width=10)
stop_button.grid(row=1, column=1, pady=20)

# Create an exit button
exit_button = tk.Button(frame, text="Exit", font=("Helvetica", 12), command=on_closing, width=10)
exit_button.grid(row=2, column=0, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
