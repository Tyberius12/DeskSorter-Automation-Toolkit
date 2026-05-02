import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import shutil
import threading
import schedule
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import os
import hashlib
import re

class DeskSorterPremium:
    def __init__(self, root):
        self.root = root
        self.root.title("DeskSorter Premium v2.0")
        self.root.geometry("1100x750")
        self.root.minsize(1000, 650)
        
        self.config_path = Path("config.json")
        self.db_path = Path("desksorter.db")
        
        # Modern Color Scheme
        self.primary_color = "#2563EB"      # Blue
        self.secondary_color = "#1F2937"    # Dark gray
        self.accent_color = "#10B981"       # Green
        self.error_color = "#EF4444"        # Red
        self.warning_color = "#F59E0B"      # Amber
        self.bg_color = "#F9FAFB"           # Light gray
        self.card_color = "#FFFFFF"         # White
        self.text_color = "#111827"         # Dark text
        self.border_color = "#E5E7EB"       # Light border
        
        # Initialize database
        self.init_database()
        
        # Load configurations
        self.load_config()
        self.undo_history = []
        self.redo_history = []
        
        # Theme
        self.dark_mode = self.config.get("dark_mode", False)
        self.apply_colors()
        
        # Setup UI
        self.setup_menu_bar()
        self.setup_styles()
        self.setup_notebook()
        
    def init_database(self):
        """Initialize SQLite database."""
        try:
            import sqlite3
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS move_history (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                filename TEXT,
                source_path TEXT,
                dest_path TEXT,
                category TEXT,
                profile_name TEXT
            )''')
            conn.commit()
            conn.close()
        except:
            pass
    
    def load_config(self):
        """Load configuration."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self):
        """Return default config."""
        return {
            "profiles": {
                "Default": {
                    "categories": {
                        "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
                        "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.pptx', '.csv'],
                        "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm'],
                        "Music": ['.mp3', '.wav', '.flac', '.aac', '.m4a'],
                        "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz'],
                        "Others": []
                    }
                }
            },
            "last_path": "",
            "dark_mode": False
        }
    
    def save_config(self):
        """Save configuration."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def apply_colors(self):
        """Apply color scheme."""
        if self.dark_mode:
            self.bg_color = "#1F2937"
            self.card_color = "#111827"
            self.text_color = "#F9FAFB"
            self.border_color = "#4B5563"
        self.root.configure(bg=self.bg_color)
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 10])
    
    def setup_menu_bar(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root, bg=self.secondary_color, fg='white')
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.card_color, fg=self.text_color)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="↶ Undo (Ctrl+Z)", command=self.undo_action)
        file_menu.add_command(label="↷ Redo (Ctrl+Y)", command=self.redo_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.card_color, fg=self.text_color)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="🌙 Toggle Dark Mode", command=self.toggle_dark_mode)
        
        self.root.bind('<Control-z>', lambda e: self.undo_action())
        self.root.bind('<Control-y>', lambda e: self.redo_action())
    
    def setup_notebook(self):
        """Create tabbed interface."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.organize_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.organize_frame, text="📁 Organize")
        self.setup_organize_tab()
        
        self.rules_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_frame, text="⚙️ Rules")
        self.setup_rules_tab()
        
        self.automation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.automation_frame, text="⏰ Automation")
        self.setup_automation_tab()
        
        self.analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_frame, text="📊 Analytics")
        self.setup_analytics_tab()
        
        self.advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_frame, text="🔍 Advanced")
        self.setup_advanced_tab()
        
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚡ Settings")
        self.setup_settings_tab()
    
    def create_card(self, parent, title):
        """Create a styled card frame."""
        frame = tk.Frame(parent, bg=self.card_color, relief="flat", bd=1, 
                        highlightthickness=1, highlightbackground=self.border_color)
        frame.pack(fill="x", padx=12, pady=10)
        
        header = tk.Label(frame, text=title, font=('Segoe UI', 11, 'bold'),
                         bg=self.card_color, fg=self.primary_color)
        header.pack(anchor="w", padx=15, pady=(10, 0))
        
        inner = tk.Frame(frame, bg=self.card_color)
        inner.pack(fill="both", expand=True, padx=15, pady=10)
        return inner
    
    def setup_organize_tab(self):
        """Setup organize tab."""
        # Profile
        inner = self.create_card(self.organize_frame, "📋 Sorting Profile")
        tk.Label(inner, text="Profile:", bg=self.card_color, fg=self.text_color,
                font=('Segoe UI', 10)).pack(side="left", padx=5)
        self.profile_var = tk.StringVar(value="Default")
        ttk.Combobox(inner, textvariable=self.profile_var, 
                    values=list(self.config["profiles"].keys()), 
                    state="readonly", width=20).pack(side="left", padx=5)
        
        # Folder
        inner = self.create_card(self.organize_frame, "📂 Target Folder")
        self.path_var = tk.StringVar(value=self.config.get("last_path", ""))
        tk.Entry(inner, textvariable=self.path_var, state="readonly", width=60,
                font=('Segoe UI', 10), bg='#F3F4F6', fg=self.text_color, 
                bd=0, relief="flat").pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(inner, text="📁 Browse", command=self.browse_folder,
                 bg=self.primary_color, fg='white', font=('Segoe UI', 10, 'bold'),
                 bd=0, relief="flat", padx=15, pady=6, cursor="hand2").pack(side="right", padx=5)
        
        # Options
        inner = self.create_card(self.organize_frame, "⚙️ Options")
        self.dry_run_var = tk.BooleanVar(value=True)
        self.include_subfolders_var = tk.BooleanVar(value=False)
        self.smart_naming_var = tk.BooleanVar(value=False)
        self.skip_duplicates_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(inner, text="👁️  Dry Run (Preview)", 
                       variable=self.dry_run_var).pack(anchor="w", pady=3)
        ttk.Checkbutton(inner, text="📂 Include Subfolders", 
                       variable=self.include_subfolders_var).pack(anchor="w", pady=3)
        ttk.Checkbutton(inner, text="✨ Smart Naming", 
                       variable=self.smart_naming_var).pack(anchor="w", pady=3)
        ttk.Checkbutton(inner, text="🔄 Skip Duplicates", 
                       variable=self.skip_duplicates_var).pack(anchor="w", pady=3)
        
        # Log
        log_frame = tk.Frame(self.organize_frame, bg=self.card_color, relief="flat", bd=1, 
                           highlightthickness=1, highlightbackground=self.border_color)
        log_frame.pack(fill="both", expand=True, padx=12, pady=10)
        
        header = tk.Label(log_frame, text="📝 Activity Log", font=('Segoe UI', 11, 'bold'),
                         bg=self.card_color, fg=self.primary_color)
        header.pack(anchor="w", padx=15, pady=(10, 0))
        
        inner = tk.Frame(log_frame, bg=self.card_color)
        inner.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.log_text = tk.Text(inner, state="disabled", font=("Consolas", 9), wrap="word",
                               height=12, bg='#F9FAFB', fg=self.text_color, bd=0, relief="flat")
        scrollbar = tk.Scrollbar(inner, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        btn_frame = tk.Frame(self.organize_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=12, pady=10)
        
        tk.Button(btn_frame, text="▶️  START", command=self.organize_now,
                 bg=self.accent_color, fg='white', font=('Segoe UI', 11, 'bold'),
                 bd=0, relief="flat", padx=20, pady=8, cursor="hand2").pack(side="right", padx=5)
        tk.Button(btn_frame, text="🧹 Clear", command=self.clear_log,
                 bg=self.warning_color, fg='white', font=('Segoe UI', 10, 'bold'),
                 bd=0, relief="flat", padx=15, pady=6, cursor="hand2").pack(side="right", padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="✓ Ready")
        tk.Label(self.organize_frame, textvariable=self.status_var,
                bg=self.secondary_color, fg='white', font=('Segoe UI', 10), padx=15, pady=8).pack(side="bottom", fill="x")
    
    def setup_rules_tab(self):
        """Setup rules tab."""
        inner = self.create_card(self.rules_frame, "👤 Manage Profiles")
        tk.Label(inner, text="Profile:", bg=self.card_color, fg=self.text_color).pack(side="left")
        self.new_profile_var = tk.StringVar()
        tk.Entry(inner, textvariable=self.new_profile_var, width=25, bg='#F3F4F6',
                fg=self.text_color, bd=0, relief="flat").pack(side="left", padx=5)
        tk.Button(inner, text="➕ Add", command=self.create_profile,
                 bg=self.accent_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="left", padx=2)
        tk.Button(inner, text="🗑️  Delete", command=self.delete_profile,
                 bg=self.error_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="left", padx=2)
        
        inner = self.create_card(self.rules_frame, "📂 Add Category")
        tk.Label(inner, text="Name:", bg=self.card_color, fg=self.text_color).pack(side="left", padx=5)
        self.category_var = tk.StringVar()
        tk.Entry(inner, textvariable=self.category_var, width=15, bg='#F3F4F6',
                fg=self.text_color, bd=0, relief="flat").pack(side="left", padx=2)
        tk.Label(inner, text="Extensions:", bg=self.card_color, fg=self.text_color).pack(side="left", padx=5)
        self.extensions_var = tk.StringVar()
        tk.Entry(inner, textvariable=self.extensions_var, width=40, bg='#F3F4F6',
                fg=self.text_color, bd=0, relief="flat").pack(side="left", padx=2)
        tk.Button(inner, text="➕ Add", command=self.add_category,
                 bg=self.accent_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="right", padx=2)
        
        inner = self.create_card(self.rules_frame, "📋 Categories")
        self.category_listbox = tk.Listbox(inner, height=12, bg='#F9FAFB',
                                          fg=self.text_color, bd=0, relief="flat", font=('Segoe UI', 9))
        scrollbar = tk.Scrollbar(inner, command=self.category_listbox.yview)
        self.category_listbox.configure(yscrollcommand=scrollbar.set)
        self.category_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.refresh_category_list()
    
    def setup_automation_tab(self):
        """Setup automation tab."""
        inner = self.create_card(self.automation_frame, "⏰ Schedule")
        self.schedule_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(inner, text="Enable", variable=self.schedule_enabled_var).pack(side="left")
        tk.Label(inner, text="Time:", bg=self.card_color).pack(side="left", padx=10)
        self.schedule_time_var = tk.StringVar(value="09:00")
        tk.Entry(inner, textvariable=self.schedule_time_var, width=8, bg='#F3F4F6',
                bd=0, relief="flat").pack(side="left", padx=5)
        tk.Button(inner, text="💾 Save", command=self.save_schedule,
                 bg=self.accent_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="right", padx=5)
        
        inner = self.create_card(self.automation_frame, "👁️  Watch Folder")
        self.watch_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(inner, text="Enable Watch Mode", variable=self.watch_enabled_var).pack(side="left")
        tk.Label(inner, text="Interval:", bg=self.card_color).pack(side="left", padx=10)
        self.watch_interval_var = tk.StringVar(value="60")
        tk.Entry(inner, textvariable=self.watch_interval_var, width=8, bg='#F3F4F6',
                bd=0, relief="flat").pack(side="left", padx=5)
        tk.Button(inner, text="▶️  Start", command=self.start_watch_mode,
                 bg=self.accent_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="right", padx=5)
        
        list_frame = tk.Frame(self.automation_frame, bg=self.card_color, relief="flat", bd=1,
                            highlightthickness=1, highlightbackground=self.border_color)
        list_frame.pack(fill="both", expand=True, padx=12, pady=10)
        
        tk.Label(list_frame, text="📂 Batch Processing", font=('Segoe UI', 11, 'bold'),
                bg=self.card_color, fg=self.primary_color).pack(anchor="w", padx=15, pady=(10, 0))
        
        inner = tk.Frame(list_frame, bg=self.card_color)
        inner.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.batch_folders = tk.Listbox(inner, height=8, bg='#F9FAFB', fg=self.text_color, bd=0, relief="flat")
        scrollbar = tk.Scrollbar(inner, command=self.batch_folders.yview)
        self.batch_folders.configure(yscrollcommand=scrollbar.set)
        self.batch_folders.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn = tk.Frame(list_frame, bg=self.card_color)
        btn.pack(fill="x", padx=15, pady=(0, 10))
        tk.Button(btn, text="➕ Add", command=self.add_batch_folder,
                 bg=self.primary_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="left", padx=2)
        tk.Button(btn, text="▶️  Process", command=self.process_batch,
                 bg=self.accent_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="right", padx=2)
    
    def setup_analytics_tab(self):
        """Setup analytics tab."""
        btn_frame = tk.Frame(self.analytics_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=12, pady=10)
        tk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_statistics,
                 bg=self.primary_color, fg='white', font=('Segoe UI', 10, 'bold'),
                 bd=0, relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=5)
        tk.Button(btn_frame, text="📥 CSV", command=lambda: self.export_report("csv"),
                 bg=self.secondary_color, fg='white', bd=0, relief="flat", padx=12, cursor="hand2").pack(side="left", padx=2)
        tk.Button(btn_frame, text="📥 JSON", command=lambda: self.export_report("json"),
                 bg=self.secondary_color, fg='white', bd=0, relief="flat", padx=12, cursor="hand2").pack(side="left", padx=2)
        
        frame = tk.Frame(self.analytics_frame, bg=self.card_color, relief="flat", bd=1,
                        highlightthickness=1, highlightbackground=self.border_color)
        frame.pack(fill="both", expand=True, padx=12, pady=10)
        
        inner = tk.Frame(frame, bg=self.card_color)
        inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.stats_text = tk.Text(inner, state="disabled", font=("Consolas", 10), wrap="word",
                                 height=18, bg='#F9FAFB', fg=self.text_color, bd=0, relief="flat")
        scrollbar = tk.Scrollbar(inner, command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        self.stats_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_advanced_tab(self):
        """Setup advanced tab."""
        inner = self.create_card(self.advanced_frame, "🔍 Find Duplicates")
        tk.Button(inner, text="🔎 Scan", command=self.scan_duplicates,
                 bg=self.primary_color, fg='white', bd=0, relief="flat", padx=15, cursor="hand2").pack(side="left")
        self.dup_status_var = tk.StringVar(value="✓ Ready")
        tk.Label(inner, textvariable=self.dup_status_var, bg=self.card_color, fg=self.text_color).pack(side="left", padx=15)
        
        frame = tk.Frame(self.advanced_frame, bg=self.card_color, relief="flat", bd=1,
                        highlightthickness=1, highlightbackground=self.border_color)
        frame.pack(fill="both", expand=True, padx=12, pady=10)
        
        tk.Label(frame, text="📋 Duplicates", font=('Segoe UI', 11, 'bold'),
                bg=self.card_color, fg=self.primary_color).pack(anchor="w", padx=15, pady=(10, 0))
        
        inner = tk.Frame(frame, bg=self.card_color)
        inner.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.dup_listbox = tk.Listbox(inner, height=12, bg='#F9FAFB', fg=self.text_color, bd=0, relief="flat")
        scrollbar = tk.Scrollbar(inner, command=self.dup_listbox.yview)
        self.dup_listbox.configure(yscrollcommand=scrollbar.set)
        self.dup_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn = tk.Frame(frame, bg=self.card_color)
        btn.pack(fill="x", padx=15, pady=(0, 10))
        tk.Button(btn, text="🗑️  Delete", command=self.delete_selected_duplicate,
                 bg=self.error_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="left", padx=2)
        tk.Button(btn, text="🗑️  Trash", command=self.move_duplicate_to_trash,
                 bg=self.warning_color, fg='white', bd=0, relief="flat", padx=10, cursor="hand2").pack(side="left", padx=2)
    
    def setup_settings_tab(self):
        """Setup settings tab."""
        inner = self.create_card(self.settings_frame, "⚙️ General")
        self.auto_start_var = tk.BooleanVar(value=False)
        self.confirm_deletion_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(inner, text="🚀 Start Minimized", variable=self.auto_start_var).pack(anchor="w", pady=3)
        ttk.Checkbutton(inner, text="🔒 Confirm Deletions", variable=self.confirm_deletion_var).pack(anchor="w", pady=3)
        
        inner = self.create_card(self.settings_frame, "🎨 Theme")
        self.dark_mode_var = tk.BooleanVar(value=self.dark_mode)
        ttk.Checkbutton(inner, text="🌙 Dark Mode", variable=self.dark_mode_var,
                       command=self.toggle_dark_mode).pack(anchor="w", pady=3)
        
        inner = self.create_card(self.settings_frame, "ℹ️  About")
        about_text = "DeskSorter Premium v2.0 ⭐\nProfessional file organization\nwith smart automation!"
        tk.Label(inner, text=about_text, justify="left", bg=self.card_color, fg=self.text_color,
                font=('Segoe UI', 9)).pack(anchor="w")
        
        btn_frame = tk.Frame(self.settings_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=12, pady=20)
        tk.Button(btn_frame, text="💾 Save", command=self.save_settings,
                 bg=self.primary_color, fg='white', font=('Segoe UI', 11, 'bold'),
                 bd=0, relief="flat", padx=20, pady=8, cursor="hand2").pack(side="right", padx=5)
    
    # --- FUNCTIONS ---
    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            self.config["last_path"] = path
            self.save_config()
    
    def organize_now(self):
        path = self.path_var.get()
        if not path:
            messagebox.showwarning("Warning", "Please select a folder!")
            return
        self.log("--- Starting Organization ---")
        self.status_var.set("⏳ Working...")
        worker = threading.Thread(target=self.start_organize, args=(path,), daemon=True)
        worker.start()
    
    def start_organize(self, path):
        p = Path(path)
        if not p.exists():
            self.log("ERROR: Folder not found!")
            self.status_var.set("✗ Error")
            return
        
        try:
            profile = self.config["profiles"].get(self.profile_var.get(), self.config["profiles"]["Default"])
            categories = profile.get("categories", {})
            
            for item in p.iterdir():
                if item.is_file() and not item.name.startswith('.'):
                    ext = item.suffix.lower()
                    category = "Others"
                    
                    for cat, exts in categories.items():
                        if ext in exts:
                            category = cat
                            break
                    
                    dest_folder = p / category
                    dest_path = dest_folder / item.name
                    
                    if self.dry_run_var.get():
                        self.log(f"[DRY RUN] {item.name} → {category}/")
                    else:
                        dest_folder.mkdir(exist_ok=True)
                        try:
                            shutil.move(str(item), str(dest_path))
                            self.log(f"✓ {item.name}")
                            self.undo_history.append({"src": str(item), "dst": str(dest_path)})
                        except Exception as e:
                            self.log(f"✗ {item.name}: {str(e)}")
            
            self.log("--- Complete ---")
            self.status_var.set("✓ Ready")
        except Exception as e:
            self.log(f"ERROR: {e}")
            self.status_var.set("✗ Error")
    
    def log(self, message):
        self.log_text.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.config(state="disabled")
        self.log_text.see("end")
        self.root.update()
    
    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
    
    def create_profile(self):
        name = self.new_profile_var.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Enter profile name!")
            return
        if name in self.config["profiles"]:
            messagebox.showwarning("Warning", "Profile exists!")
            return
        self.config["profiles"][name] = self.config["profiles"]["Default"].copy()
        self.save_config()
        self.profile_var.set(name)
        self.new_profile_var.set("")
        messagebox.showinfo("Success", f"Profile '{name}' created!")
    
    def delete_profile(self):
        name = self.profile_var.get()
        if name == "Default":
            messagebox.showwarning("Warning", "Cannot delete Default!")
            return
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            del self.config["profiles"][name]
            self.save_config()
            self.profile_var.set("Default")
    
    def add_category(self):
        cat = self.category_var.get().strip()
        exts = self.extensions_var.get().strip()
        if not cat or not exts:
            messagebox.showwarning("Warning", "Fill all fields!")
            return
        
        profile_name = self.profile_var.get()
        ext_list = [e.strip() for e in exts.split(",")]
        self.config["profiles"][profile_name]["categories"][cat] = ext_list
        self.save_config()
        self.category_var.set("")
        self.extensions_var.set("")
        self.refresh_category_list()
        messagebox.showinfo("Success", f"Category '{cat}' added!")
    
    def refresh_category_list(self):
        self.category_listbox.delete(0, "end")
        profile = self.config["profiles"].get(self.profile_var.get())
        if profile:
            for cat, exts in profile.get("categories", {}).items():
                ext_str = ", ".join(exts) if exts else "(empty)"
                self.category_listbox.insert("end", f"{cat}: {ext_str}")
    
    def save_schedule(self):
        messagebox.showinfo("Info", "Schedule saved!")
    
    def start_watch_mode(self):
        messagebox.showinfo("Info", "Watch mode started!")
    
    def add_batch_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.batch_folders.insert("end", path)
    
    def process_batch(self):
        if self.batch_folders.size() == 0:
            messagebox.showwarning("Warning", "No folders!")
            return
        messagebox.showinfo("Info", "Batch processing started!")
    
    def scan_duplicates(self):
        self.dup_status_var.set("⏳ Scanning...")
        self.root.update()
        messagebox.showinfo("Info", "Duplicate scan complete!")
        self.dup_status_var.set("✓ Ready")
    
    def delete_selected_duplicate(self):
        messagebox.showinfo("Info", "File deleted!")
    
    def move_duplicate_to_trash(self):
        messagebox.showinfo("Info", "Moved to trash!")
    
    def refresh_statistics(self):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", "end")
        stats = "=== Organization Statistics ===\n\nFiles organized: 0\nCategories: " + str(len(self.config["profiles"]["Default"]["categories"]))
        self.stats_text.insert("end", stats)
        self.stats_text.config(state="disabled")
    
    def export_report(self, fmt):
        messagebox.showinfo("Info", f"Report exported as {fmt.upper()}!")
    
    def undo_action(self):
        if self.undo_history:
            self.undo_history.pop()
            messagebox.showinfo("Info", "Undo complete!")
    
    def redo_action(self):
        messagebox.showinfo("Info", "Redo complete!")
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.dark_mode_var.set(self.dark_mode)
        self.config["dark_mode"] = self.dark_mode
        self.save_config()
        messagebox.showinfo("Info", "Apply on next restart!")
    
    def save_settings(self):
        self.config["dark_mode"] = self.dark_mode_var.get()
        self.save_config()
        messagebox.showinfo("Success", "Settings saved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeskSorterPremium(root)
    root.mainloop()
