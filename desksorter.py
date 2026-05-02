import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import shutil
import threading
from pathlib import Path
from datetime import datetime

class DeskSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeskSorter v1.1 - Premium Capstone")
        self.root.geometry("600x650")
        self.config_path = Path("config.json")
        
        # Professional Styling - "Clam" theme offers a cleaner, flatter look
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # File Categorization Rules (The "Brain")
        self.categories = {
            "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.pptx', '.csv'],
            "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm'],
            "Music": ['.mp3', '.wav', '.flac', '.aac', '.m4a'],
            "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz'],
        }
        
        self.setup_ui()
        self.load_last_path()

    def setup_ui(self):
        """Builds the User Interface with Progress Tracking and Styling."""
        # --- HEADER SECTION ---
        header = tk.Frame(self.root, pady=15, bg="#f8f9fa")
        header.pack(fill="x", padx=10)
        
        self.path_var = tk.StringVar()
        tk.Label(header, text="Target Folder:", font=("Arial", 10, "bold"), bg="#f8f9fa").pack(side="left")
        tk.Entry(header, textvariable=self.path_var, state="readonly").pack(side="left", fill="x", expand=True, padx=10)
        tk.Button(header, text="Browse", command=self.browse_folder, width=10).pack(side="right")

        # --- OPTIONS SECTION ---
        options = tk.Frame(self.root, pady=10)
        options.pack(fill="x", padx=15)
        
        self.dry_run_var = tk.BooleanVar(value=True) # Defaulting to safe mode
        tk.Checkbutton(options, text="Dry Run (Preview Only)", variable=self.dry_run_var, font=("Arial", 9)).pack(side="left")
        
        tk.Button(options, text="START ORGANIZING", command=self.organize_now, 
                  bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10).pack(side="right")

        # --- PROGRESS TRACKING (Premium Feature) ---
        prog_frame = tk.Frame(self.root, pady=15)
        prog_frame.pack(fill="x", padx=15)
        
        # Determinate Progress Bar linked to progress_var
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(prog_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x")
        
        # Numerical tracking (e.g., 5 / 20 files)
        self.counter_var = tk.StringVar(value="Waiting to scan...")
        tk.Label(prog_frame, textvariable=self.counter_var, font=("Arial", 9, "italic")).pack(pady=5)

        # --- LOGGING SECTION (Scrollable) ---
        tk.Label(self.root, text="Activity Log:", font=("Arial", 10, "bold")).pack(anchor="w", padx=15)
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.log_text = tk.Text(log_frame, state="disabled", font=("Consolas", 9), wrap="word", bg="#fcfcfc")
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- STATUS BAR ---
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", padx=10)
        status_bar.pack(side="bottom", fill="x")

    def log(self, message):
        """Thread-safe logging with formatted timestamps."""
        self.log_text.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def browse_folder(self):
        """User interaction to select folder and persist state."""
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            try:
                with open(self.config_path, 'w') as f:
                    json.dump({"last_path": path}, f)
            except Exception as e:
                self.log(f"Config Warning: {e}")

    def load_last_path(self):
        """Loads persistence data from config.json on startup."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.path_var.set(data.get("last_path", ""))
            except: pass 

    def organize_now(self):
        """Entry point for organization. Launches background thread to avoid UI freezing."""
        path = self.path_var.get()
        if not path:
            messagebox.showwarning("Input Error", "Please select a target folder first.")
            return

        self.log("--- Initializing Organization Worker ---")
        self.status_var.set("Working...")
        self.progress_var.set(0) # Reset UI state
        
        worker = threading.Thread(target=self.start_logic, args=(path,), daemon=True)
        worker.start()

    def start_logic(self, path):
        """The core Engine that executes file movement and updates the progress bar[cite: 1]."""
        p = Path(path)
        if not p.exists() or not p.is_dir():
            self.log("CRITICAL: Invalid or inaccessible path.")
            return

        # Pre-count files for the determinate progress bar
        items_to_move = [i for i in p.iterdir() if i.is_file() and not i.name.startswith('.')]
        total_files = len(items_to_move)
        
        if total_files == 0:
            self.log("No files found to organize.")
            self.counter_var.set("Scanning finished (0 files).")
            self.status_var.set("Ready")
            return

        processed_count = 0

        try:
            for item in items_to_move:
                ext = item.suffix.lower()
                category = "Others"
                
                for cat, exts in self.categories.items():
                    if ext in exts:
                        category = cat
                        break
                
                dest_folder = p / category
                dest_path = dest_folder / item.name

                if self.dry_run_var.get():
                    self.log(f"[DRY RUN] Would move {item.name} to {category}/")
                else:
                    dest_folder.mkdir(exist_ok=True)
                    try:
                        # shutil.move handles cross-drive operations better than os.rename[cite: 1]
                        shutil.move(str(item), str(dest_path))
                        self.log(f"MOVED: {item.name}")
                    except Exception as e:
                        self.log(f"SKIPPED: {item.name} (File in use/Access denied)")

                # Update progress bar and counter label
                processed_count += 1
                progress_percentage = (processed_count / total_files) * 100
                self.progress_var.set(progress_percentage)
                self.counter_var.set(f"Completed: {processed_count} / {total_files} files")
                
            self.log(f"--- Task Complete: {processed_count} files handled ---")
            self.status_var.set("Done")
            messagebox.showinfo("Organization Complete", f"Successfully processed {total_files} files.")
            
        except Exception as e:
            self.log(f"ENGINE ERROR: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeskSorterApp(root)
    root.mainloop() # Essential main event loop for GUI persistence[cite: 1]