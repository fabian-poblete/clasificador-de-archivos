import os
import time
import tkinter as tk
from tkinter import filedialog
from threading import Thread

# Create the main window
root = tk.Tk()
root.title("File Classifier")



# Global variable to store the selected directory
directory = None

# Function to handle the button click event
def select_directory():
    global directory
    # Open a file dialog to select the directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        if directory is None:
            # First time selecting the directory
            # Update the directory variable
            directory = selected_directory
            # Show the selected directory in the text widget
            output_text.insert(tk.END, f'Selected directory: {directory}\n')
            # Disable the select button and enable the change button
            select_button.config(text='Change Directory')
        else:
            # Changing the directory
            # Clear the text widget
            output_text.delete(1.0, tk.END)
            # Update the directory variable
            directory = selected_directory
            # Show the selected directory in the text widget
            output_text.insert(tk.END, f'Changed directory: {directory}\n')
        # Classify all existing files in the directory
        classify_files_in_directory()
        # Start monitoring the directory for changes in a separate thread
        thread = Thread(target=monitor_directory)
        thread.start()

# Create a button to select/change the directory
select_button = tk.Button(root, text='Seleccionar carpeta', command=select_directory)
select_button.pack()

# Create a text widget to display the output
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

# Function to classify a file
def classify_file(filename):
    # Find the file extension
    extension = filename.split('.')[-1]

    # Iterate over the categories
    for category, extensions in categories.items():
        # If the extension matches one of the extensions in the category, move the file
        if extension in extensions:
            # Construct the file paths
            source_path = os.path.join(directory, filename)
            dest_path = os.path.join(directory, category, filename)

            # Move the file
            os.rename(source_path, dest_path)
            output_text.insert(tk.END, f'Moved {filename} to {category}\n')
            break

# Function to classify all existing files in the directory
def classify_files_in_directory():
    # Clear the text widget
    output_text.delete(1.0, tk.END)
    for filename in os.listdir(directory):
        classify_file(filename)

# Function to monitor the directory for changes
def monitor_directory():
    # Initial list of files in the directory
    initial_files = os.listdir(directory)

    while True:
        # List of files in the directory after a short sleep
        time.sleep(5)
        current_files = os.listdir(directory)

        # Find the new files
        new_files = list(set(current_files) - set(initial_files))

        # Classify the new files
        for filename in new_files:
            classify_file(filename)

        # Update the initial list of files
        initial_files = current_files

# Dictionary of file categories and their extensions
categories = {
    'Images': ['jpeg', 'jpg', 'png', 'jfif'],
    'PDFs': ['pdf'],
    'Datasets': ['csv', 'xlsx', 'json'],
    'Videos': ['mp4'],
    'Words': ['docx'],
    'Executable': ['exe'],
    'Direct access': ['lnk'],
}

# Run the main window event loop
root.mainloop()
