#!/usr/bin/env python
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk

def run_cli():
    root.destroy()
    print("Starting CLI version...")
    try:
        subprocess.run([sys.executable, "detect.py"])
    except Exception as e:
        print(f"Error running CLI version: {e}")
    input("Press Enter to exit...")

def run_gui():
    root.destroy()
    print("Starting GUI version...")
    try:
        subprocess.run([sys.executable, "gui.py"])
    except Exception as e:
        print(f"Error running GUI version: {e}")
        input("Press Enter to exit...")

# Create launcher window
root = tk.Tk()
root.title("Intrusion Detection System - Launcher")
root.geometry("400x200")

# Style
style = ttk.Style()
style.configure("TButton", font=("Arial", 12))

# Main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
ttk.Label(
    main_frame,
    text="Intrusion Detection System",
    font=("Arial", 16, "bold")
).pack(pady=10)

ttk.Label(
    main_frame,
    text="Choose how to run the application:",
    font=("Arial", 11)
).pack(pady=10)

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

ttk.Button(
    button_frame,
    text="Command Line Interface",
    command=run_cli,
    width=25
).pack(side=tk.LEFT, padx=10)

ttk.Button(
    button_frame,
    text="Graphical User Interface",
    command=run_gui,
    width=25
).pack(side=tk.LEFT, padx=10)

# Run the launcher
if __name__ == "__main__":
    root.mainloop() 