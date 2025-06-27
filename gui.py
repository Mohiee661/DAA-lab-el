import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import time
import os
from detect import load_signatures, load_data, detect_intrusions
from kmp import kmp_search
from naive_search import naive_search

class IntrusionDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intrusion Detection System")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # File selection area
        self.setup_file_selection()
        
        # Signatures area
        self.setup_signatures_area()
        
        # Log file preview area
        self.setup_log_preview()
        
        # Results area
        self.setup_results_area()
        
        # Action buttons
        self.setup_action_buttons()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize default values
        self.signatures_file = "signatures.txt"
        self.log_file = "sample_log.txt"
        self.load_default_files()

    def setup_file_selection(self):
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)

        # Signatures file
        ttk.Label(file_frame, text="Signatures File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.signatures_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.signatures_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_signatures).grid(row=0, column=2, padx=5, pady=5)

        # Log file
        ttk.Label(file_frame, text="Log File:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.log_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.log_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_log_file).grid(row=1, column=2, padx=5, pady=5)
    
    def setup_signatures_area(self):
        signatures_frame = ttk.LabelFrame(self.main_frame, text="Signatures", padding="10")
        signatures_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.signatures_text = scrolledtext.ScrolledText(signatures_frame, wrap=tk.WORD, width=40, height=6)
        self.signatures_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_log_preview(self):
        log_frame = ttk.LabelFrame(self.main_frame, text="Log File Preview", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=40, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_results_area(self):
        results_frame = ttk.LabelFrame(self.main_frame, text="Detection Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create notebook with tabs for KMP and Naive search results
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # KMP tab
        kmp_frame = ttk.Frame(self.results_notebook, padding="10")
        self.results_notebook.add(kmp_frame, text="KMP Search Results")
        
        self.kmp_results_text = scrolledtext.ScrolledText(kmp_frame, wrap=tk.WORD, width=40, height=8)
        self.kmp_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Naive search tab
        naive_frame = ttk.Frame(self.results_notebook, padding="10")
        self.results_notebook.add(naive_frame, text="Naive Search Results")
        
        self.naive_results_text = scrolledtext.ScrolledText(naive_frame, wrap=tk.WORD, width=40, height=8)
        self.naive_results_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_action_buttons(self):
        button_frame = ttk.Frame(self.main_frame, padding="10")
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Detect Intrusions", command=self.run_detection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def browse_signatures(self):
        filename = filedialog.askopenfilename(
            title="Select Signatures File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.signatures_file_var.set(filename)
            self.signatures_file = filename
            self.load_signatures_content()
    
    def browse_log_file(self):
        filename = filedialog.askopenfilename(
            title="Select Log File",
            filetypes=(("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*"))
        )
        if filename:
            self.log_file_var.set(filename)
            self.log_file = filename
            self.load_log_content()
    
    def load_default_files(self):
        self.signatures_file_var.set(self.signatures_file)
        self.log_file_var.set(self.log_file)
        self.load_signatures_content()
        self.load_log_content()
    
    def load_signatures_content(self):
        try:
            with open(self.signatures_file, 'r') as f:
                content = f.read()
                self.signatures_text.delete(1.0, tk.END)
                self.signatures_text.insert(tk.END, content)
        except Exception as e:
            self.status_var.set(f"Error loading signatures: {str(e)}")
            messagebox.showerror("Error", f"Could not load signatures file: {str(e)}")
    
    def load_log_content(self):
        try:
            with open(self.log_file, 'r') as f:
                content = f.read()
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, content)
        except Exception as e:
            self.status_var.set(f"Error loading log file: {str(e)}")
            messagebox.showerror("Error", f"Could not load log file: {str(e)}")
    
    def run_detection(self):
        try:
            self.status_var.set("Running detection...")
            self.root.update()
            
            # Load signatures and data
            signatures = load_signatures(self.signatures_file)
            data = load_data(self.log_file)
            
            # Run KMP detection
            start_time = time.time()
            kmp_results = detect_intrusions(data, signatures, kmp_search)
            kmp_time = time.time() - start_time
            
            # Run Naive detection
            start_time = time.time()
            naive_results = detect_intrusions(data, signatures, naive_search)
            naive_time = time.time() - start_time
            
            # Display KMP results
            self.kmp_results_text.delete(1.0, tk.END)
            for signature, matches in kmp_results.items():
                self.kmp_results_text.insert(tk.END, f"Signature: {signature}\n")
                self.kmp_results_text.insert(tk.END, f"Matches at positions: {matches}\n\n")
            self.kmp_results_text.insert(tk.END, f"KMP Time: {kmp_time:.6f} seconds\n")
            
            # Display Naive results
            self.naive_results_text.delete(1.0, tk.END)
            for signature, matches in naive_results.items():
                self.naive_results_text.insert(tk.END, f"Signature: {signature}\n")
                self.naive_results_text.insert(tk.END, f"Matches at positions: {matches}\n\n")
            self.naive_results_text.insert(tk.END, f"Naive Search Time: {naive_time:.6f} seconds\n")
            
            self.status_var.set("Detection completed")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Detection failed: {str(e)}")
    
    def clear_results(self):
        self.kmp_results_text.delete(1.0, tk.END)
        self.naive_results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")


if __name__ == "__main__":
    root = tk.Tk()
    app = IntrusionDetectionGUI(root)
    root.mainloop() 