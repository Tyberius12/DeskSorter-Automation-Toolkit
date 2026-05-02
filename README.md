# DeskSorter Premium v2.0 - Comprehensive Desktop Organization Suite

**DeskSorter** is a professional-grade desktop automation toolkit built with Python and Tkinter. It transforms cluttered directories into organized hubs by intelligently categorizing files based on extensions, with advanced features including automated scheduling, duplicate detection, customizable rules, and a full-featured analytics dashboard.

**Current Version:** 2.0 (May 2, 2026)  
**License:** Open Source  
**Platform Support:** Windows, macOS, Linux  

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Core Architecture](#core-architecture)
6. [Usage Guide](#usage-guide)
7. [Configuration](#configuration)
8. [Database & History](#database--history)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [FAQ & Troubleshooting](#faq--troubleshooting)
11. [Development](#development)

---

## 🎯 Overview

DeskSorter Premium is a next-generation file organization system designed with both casual users and power users in mind. The application combines a user-friendly graphical interface with a robust backend engine capable of handling complex sorting scenarios, automated scheduling, and intelligent file management.

### Philosophy
- **Safety First**: All operations include dry run modes and undo capabilities
- **Non-blocking Operations**: Multi-threaded architecture ensures responsive UI
- **Modular Design**: Separate engine, configuration, and UI components
- **User Control**: Full transparency with activity logs and operation history

---

## ✨ Key Features

### Core Functionality
- **Automatic File Categorization**: Organize files into categories based on extension
- **Multi-threaded Engine**: Keeps the UI responsive during heavy file operations
- **Dry Run Mode**: Preview all changes before moving any files
- **Smart Persistence**: Remembers your last used folder and preferences via `config.json`
- **Determinate Progress Tracking**: Real-time progress bar with file counts (e.g., 5 / 20 files)
- **Activity Logging**: Complete audit trail with timestamps for all operations

### Advanced Features
- **Custom Sorting Rules**: Create unlimited custom categories and file type associations
- **Profile System**: Save and manage multiple sorting profiles (Default, Photos, Downloads, custom)
- **Undo/Redo System**: Reverse file movements with Ctrl+Z/Ctrl+Y
- **Duplicate Detection**: Find and handle duplicate files using MD5 hash comparison
- **Smart File Naming**: Auto-rename files with customizable patterns
- **Batch Processing**: Process multiple folders in a single operation
- **Watch Folder Mode**: Monitor folders for new files and organize automatically
- **Scheduled Automation**: Auto-organize on daily/weekly/monthly schedules

### Analytics & Reporting
- **Analytics Dashboard**: View detailed statistics about your organization
- **Move History Tracking**: Complete database of all file movements
- **CSV/JSON Export**: Export reports for spreadsheet analysis
- **Statistics Timeline**: Historical trends of file organization

### User Interface
- **Tabbed Interface**: 6 organized tabs for different functions
  1. **Organize Files** - Main organizing interface
  2. **Custom Rules** - Create/edit profiles and categories
  3. **Automation** - Scheduling and batch processing
  4. **Analytics** - Statistics and reports
  5. **Advanced** - Duplicate detection and smart naming
  6. **Settings** - User preferences and appearance
- **Dark Mode**: Professional dark theme option with persistent settings
- **Menu Bar**: File, View, and Help menus with keyboard shortcuts
- **Status Bar**: Real-time status updates during operations
- **Scrollable Activity Log**: Colored and formatted log messages with timestamps

---

## 📦 Installation

### Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd DeskSorter
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `tkinter` - Built-in Python GUI framework
- `Pillow==9.5.0` - Image handling and processing
- `send2trash==1.8.16` - Safe file deletion to recycle bin
- `schedule==1.1.9` - Task scheduling for automation
- `sqlite3` - Built-in database for history tracking

### Step 3: Run the Application

**Option A: Python Script**
```bash
python launch.py
```

**Option B: Windows Batch Script**
```bash
launch.bat
```

---

## 🚀 Quick Start

### Basic Usage (30 seconds)

1. **Launch Application**
   - Run `python launch.py` or double-click `launch.bat`
   - GUI window opens automatically

2. **Select Folder**
   - Click "Browse" button
   - Choose your target folder (Desktop, Downloads, etc.)
   - Path is automatically saved for next session

3. **Dry Run (Recommended First Time)**
   - "Dry Run (Preview Only)" checkbox is enabled by default
   - Click "START ORGANIZING"
   - View the Activity Log to see what WOULD be moved
   - Files are NOT moved during dry run

4. **Real Organization**
   - Uncheck "Dry Run (Preview Only)" 
   - Click "START ORGANIZING"
   - Progress bar fills as files are organized
   - Files are moved to category folders (Images/, Documents/, etc.)

5. **Review Results**
   - Check Activity Log for details
   - See status bar showing completion
   - Folders created automatically with discovered files

### Minimal Example (Core Logic)
```python
from pathlib import Path
import shutil

# This is what happens under the hood
target = Path("C:/Users/User/Desktop")
files = [f for f in target.iterdir() if f.is_file()]

categories = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt'],
}

for file in files:
    ext = file.suffix.lower()
    for category, extensions in categories.items():
        if ext in extensions:
            folder = target / category
            folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(folder / file.name))
            break
```

---

## 🏗️ Core Architecture

### Modular Design
The application is divided into four main components:

**UI Layer:** desksorter_premium.py
- 6-tab interface for different functions
- Event handling and user interactions
- Multi-threaded operations for responsiveness
- Status updates and activity logging

**Business Logic:** sorter_engine.py
- File organization and categorization
- Duplicate detection and hash comparison
- Smart file naming with patterns
- Statistics and move history management

**Configuration:** config_manager.py
- Profile management (create, update, delete)
- Settings persistence
- Default configurations
- User customization support

**Utilities:** utils.py
- File operations (hashing, metadata, info)
- Date/time formatting utilities
- Report generation (CSV, JSON)
- Safe filename handling

### System Components

**Configuration File (config.json)**
- User profiles and categories
- Application preferences
- Last used paths and settings
- Scheduled tasks

**Database (desksorter.db)**
- Complete move history with timestamps
- File hash tracking for duplicates
- Undo/Redo capability
- Organization statistics

### Information Flow

```
User Input → UI Layer → Business Logic → File Operations
    ↓            ↓            ↓              ↓
  GUI        Events      Sorting        Move Files
Interaction  Handling    Engine         to Folders
    ↓            ↓            ↓              ↓
              Database ← Track History ← Results
```

---

## 📖 Usage Guide

### Tab 1: Organize Files (Main Interface)

**Purpose**: Perform immediate file organization operations

**Components:**
1. **Target Folder Selection**
   - Browse button to select folder
   - Selected path shown in read-only field
   - Last used path remembered from `config.json`

2. **Dry Run Toggle (Default: ON)**
   - Preview mode enabled by default for safety
   - Uncheck to perform actual file movements
   - Useful for testing before real operations

3. **Progress Tracking**
   - Determinate progress bar (0-100%)
   - Counter showing: "Completed: 5 / 20 files"
   - Updates in real-time as files are processed

4. **Activity Log**
   - Scrollable text widget with timestamps
   - Shows each action: `[14:32:15] MOVED: document.pdf`
   - Different entry types: MOVED, SKIPPED, CRITICAL, DRY RUN
   - Color-coded (if supported by terminal)

5. **Status Bar**
   - Bottom status showing: Ready, Working..., Done
   - Updates after operations complete

**Default File Categories:**
| Category | Extensions |
|----------|-----------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt, .xlsx, .pptx, .csv |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .webm |
| **Music** | .mp3, .wav, .flac, .aac, .m4a |
| **Archives** | .zip, .rar, .7z, .tar, .gz |
| **Others** | Uncategorized files |

### Tab 2: Custom Rules

**Purpose**: Define custom sorting profiles and file categories

**Features:**
- Create unlimited custom profiles
- Clone from existing profiles (e.g., "Photos" from "Default")
- Add/remove file extensions
- Set as default profile for quick organizing
- Delete unused profiles (cannot delete "Default")

**Pre-configured Profiles:**
1. **Default** - Standard file organization
2. **Photos** - Photo library with smart naming
3. **Downloads** - Specialized for Downloads folder

### Tab 3: Automation

**Purpose**: Schedule automatic organization

**Features:**
- Daily, weekly, or monthly scheduling
- Multiple scheduled tasks
- Folder watch mode (monitor for new files)
- Batch process multiple folders
- Run at system startup (optional)

### Tab 4: Analytics

**Purpose**: View statistics and generate reports

**Features:**
- Total files organized
- Files by category breakdown
- Most common file types
- Organization timeline
- CSV export for analysis
- Storage usage by category

### Tab 5: Advanced

**Purpose**: Advanced file operations

**Features:**
- **Duplicate Detection**: Find duplicate files using hash comparison
  - Displays files with identical MD5/SHA256 hashes
  - Preview before deletion
  - Safe removal to recycle bin (send2trash)
  
- **Smart File Naming**: Auto-rename files with patterns
  - Patterns: `{name}`, `{date}`, `{hash}`
  - Example: `document.pdf` → `2026-05-02_document.pdf`
  - Preview before applying

- **File Properties**: View detailed file information
  - File size, created date, modified date
  - File hash (MD5/SHA256)
  - Full path and extension

### Tab 6: Settings

**Purpose**: Configure application preferences

**Settings:**
- **Dark Mode**: Toggle dark/light theme
- **Auto-start**: Run on system startup
- **Confirm Deletion**: Ask before moving to trash
- **Notifications**: Enable/disable notifications
- **Theme Persistence**: Remember selected theme
- **Log Level**: Verbose, Normal, or Minimal

---

## ⚙️ Configuration

### config.json Structure

```json
{
  "profiles": {
    "Default": {
      "categories": {
        "Images": [".jpg", ".jpeg", ".png", ...],
        "Documents": [".pdf", ".doc", ...],
        ...
      },
      "settings": {
        "create_subfolder": false,
        "smart_naming": false,
        "skip_duplicates": false,
        "include_subfolders": false
      }
    }
  },
  "last_path": "/Users/username/Desktop",
  "dark_mode": false,
  "auto_start": false,
  "confirm_deletion": true,
  "scheduled_tasks": []
}
```

### Configuration Options

**Profile Settings:**
- `create_subfolder` - Create category folders if they don't exist
- `smart_naming` - Auto-rename files with patterns
- `skip_duplicates` - Skip files that already exist in destination
- `include_subfolders` - Recursively organize subfolders
- `naming_pattern` - Custom pattern for smart naming

**Global Settings:**
- `dark_mode` - Apply dark theme (persistent)
- `auto_start` - Launch on system startup
- `confirm_deletion` - Confirm before moving files
- `log_level` - Verbosity of activity log

### Environment Variables (Optional)

```bash
# Custom config location
DESKSORTER_CONFIG=/path/to/config.json

# Custom database location
DESKSORTER_DB=/path/to/desksorter.db

# Debug mode
DESKSORTER_DEBUG=1
```

---

## 🗄️ Database & History

### SQLite Database (desksorter.db)

The application tracks all operations in a local SQLite database for undo/redo and analytics.

**move_history Table:**
```sql
CREATE TABLE move_history (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,              -- "2026-05-02 14:32:15"
    filename TEXT,               -- Original filename
    source_path TEXT,            -- Original full path
    dest_path TEXT,              -- Destination full path
    category TEXT,               -- Category folder
    profile_name TEXT            -- Profile used
);
```

**Queries:**
- View all moves from today: `WHERE DATE(timestamp) = DATE('now')`
- Find all PDF movements: `WHERE filename LIKE '%.pdf'`
- Undo last operation: Use `redo_history` to restore files

### Accessing History Programmatically

```python
from sorter_engine import SortingEngine

engine = SortingEngine(db_path="desksorter.db")
history = engine.get_move_history(limit=10)  # Last 10 operations
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo last operation |
| `Ctrl+Y` | Redo last operation |
| `Ctrl+O` | Open folder browser |
| `Ctrl+S` | Save configuration |
| `Ctrl+E` | Export report |
| `Ctrl+L` | Clear log |
| `Alt+D` | Toggle dark mode |
| `F1` | Show help/documentation |
| `Escape` | Cancel current operation |

---

## 🔌 Threading & Performance

### Multi-threaded Architecture

The application uses Python's `threading` module to prevent UI freezing:

```python
def organize_now(self):
    """Entry point launches background thread"""
    worker = threading.Thread(
        target=self.start_logic, 
        args=(path,), 
        daemon=True
    )
    worker.start()
```

**Benefits:**
- UI remains responsive while organizing files
- Progress bar updates in real-time
- User can cancel long operations
- Multiple operations can run simultaneously

### Performance Characteristics

- **Scanning**: 1,000 files in ~0.5 seconds
- **Moving (local drive)**: 10-50 files/second depending on size
- **Moving (network drive)**: 1-5 files/second
- **Duplicate detection**: 100 files in ~2 seconds (MD5 hashing)

**Optimization Tips:**
1. Organize local drives first (fastest)
2. Exclude unnecessary folders in settings
3. Use profiles with fewer categories for speed
4. Disable duplicate detection if not needed

---

### Adding Custom Categories

Edit `config.json` to add new extensions:
```json
{
  "profiles": {
    "Default": {
      "categories": {
        "Code": [".py", ".js", ".java", ".cpp"],
        "Data": [".csv", ".json", ".sql"]
      }
    }
  }
}
```

Or use the Custom Rules tab:

1. Click "Create New Profile"
2. Name it (e.g., "Gaming")
3. Add categories and extensions
4. Save and use

---

## ❓ FAQ & Troubleshooting

### Q: Can I undo file movements?
**A:** Yes! Use Ctrl+Z or File → Undo. The application tracks all operations in the database.

### Q: My files aren't moving. What's wrong?
**A:** 
1. Check that "Dry Run (Preview Only)" is unchecked
2. Verify file permissions (some system files are protected)
3. Check Activity Log for error messages
4. Ensure destination folders have write permissions

### Q: Can I exclude certain files?
**A:** Files starting with `.` (hidden files) are automatically excluded. Custom exclusion patterns coming in v3.0.

### Q: How do I schedule automatic organization?
**A:** Go to Automation tab, set schedule (Daily/Weekly/Monthly), select folder, and enable.

### Q: Where is my data stored?
**A:** 
- Configuration: `config.json` (same directory as application)
- Database: `desksorter.db` (same directory)
- These files are created automatically on first run

### Q: Does it work on network drives?
**A:** Yes, but performance is slower. It's optimized for local drives.

### Q: Can I sort by criteria other than file extension?
**A:** Currently extension-based only. Date-based and size-based sorting planned for v3.0.

### Q: How do I safely test before organizing?
**A:** 
1. Always check "Dry Run (Preview Only)"
2. Review Activity Log
3. Uncheck only when confident
4. Create backup of important files first

---

## � Documentation Files

For more information, see:
- **JOURNAL.md** - Development timeline, design decisions, and lessons learned
- **CHANGELOG.md** - Detailed version history and feature releases
- **QUICKSTART.md** - 5-minute quick start guide
- **ADVANCED.md** - Advanced usage scenarios
- **PROJECT_STRUCTURE.md** - Detailed architecture documentation

---

**Last Updated:** May 2, 2026 | **Version:** 2.0