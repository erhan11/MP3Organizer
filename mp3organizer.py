import os
import hashlib
import shutil
from tkinter import Tk, filedialog, messagebox, Button, Label, Frame

from mutagen.mp3 import MP3
from mutagen.id3 import ID3

# Function to get the hash of the audio file content
def get_file_hash(filepath):
    """Get the hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to find and return duplicates in a directory
def find_duplicates(directory):
    """Find and return duplicate files in the given directory."""
    seen_hashes = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)

                if file_hash in seen_hashes:
                    duplicates.append(file_path)
                else:
                    seen_hashes[file_hash] = file_path
    return duplicates

# Function to move duplicates to a chosen folder
def move_duplicates(duplicates, destination_folder):
    """Move duplicates to the chosen folder for later review."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for duplicate in duplicates:
        shutil.move(duplicate, os.path.join(destination_folder, os.path.basename(duplicate)))

# Function to handle the finding and moving of duplicates
def handle_duplicates():
    # Show an informational message to guide the user
    messagebox.showinfo("Find Duplicates", "You will now be prompted to select a folder to scan for duplicate MP3 files.")
    
    # Ask user to select the folder to scan for duplicates
    directory = filedialog.askdirectory(title="Select Folder to Scan for Duplicates")
    if not directory:
        messagebox.showwarning("No Folder Selected", "No folder was selected. Please select a folder to scan.")
        return

    # Find duplicates in the selected folder
    duplicates = find_duplicates(directory)

    if duplicates:
        # Inform user about the next step
        messagebox.showinfo("Duplicates Found", f"{len(duplicates)} duplicates found. You will now select a folder to move them.")
        
        # Ask user to select the destination folder to move duplicates
        destination_folder = filedialog.askdirectory(title="Select Folder to Move Duplicates")
        if destination_folder:
            move_duplicates(duplicates, destination_folder)
            messagebox.showinfo("Duplicates Moved", f"Moved {len(duplicates)} duplicate files.")
        else:
            messagebox.showwarning("No Folder Selected", "No folder was selected. No files were moved.")
    else:
        messagebox.showinfo("No Duplicates", "No duplicate files found.")

# Set up the GUI with a cleaner look
def setup_gui():
    root = Tk()
    root.title("MP3 Organizer")

    # Centering the window
    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
    frame = Frame(root)
    frame.pack(pady=20)

    label = Label(frame, text="MP3 Duplicate Organizer", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    button = Button(frame, text="Find and Move Duplicates", command=handle_duplicates, width=30, height=2)
    button.pack(pady=10)

    root.mainloop()

# Run the application
if __name__ == "__main__":
    setup_gui()