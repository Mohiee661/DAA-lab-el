#!/usr/bin/env python
import subprocess
import sys
import os
import webbrowser
import time
import threading

def open_browser():
    """Open browser after a short delay"""
    print("Starting web browser...")
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def run_web_app():
    print("="*50)
    print("Intrusion Detection System - Web Interface")
    print("="*50)
    print("\nStarting Flask server...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the Flask application
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    run_web_app() 