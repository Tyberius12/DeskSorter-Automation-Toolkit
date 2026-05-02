# DeskSorter Premium - Project Architecture

## Project Structure

```
DeskSorter/
├── desksorter_premium.py      # Main GUI Application (1000+ lines)
│   ├── DeskSorterPremium class
│   ├── UI Components (6 tabs)
│   ├── Event Handlers
│   └── Background Workers
│
├── sorter_engine.py            # Core Sorting Logic Module
│   ├── SortingEngine class
│   ├── File processing
│   ├── Duplicate detection
│   ├── History tracking
│   └── Statistics management
│
├── config_manager.py           # Configuration Management
│   ├── ConfigManager class
│   ├── Profile management
│   ├── Settings persistence
│   └── Default configurations
│
├── utils.py                    # Utility Functions
│   ├── FileUtils
│   ├── DateUtils
│   ├── ReportGenerator
│   ├── ValidationUtils
│   └── SystemUtils
│
├── config.json                 # Configuration & Profiles
│   ├── Profile definitions
│   ├── User preferences
│   └── Scheduled tasks
│
├── desksorter.db              # SQLite Database
│   ├── move_history table
│   └── file_hashes table
│
├── launch.bat                  # Windows Launcher Script
├── launch.py                   # Python Launcher Script
│
├── requirements.txt            # Python Dependencies
│
├── README.md                   # Full Documentation
├── QUICKSTART.md              # Quick Start Guide
├── ADVANCED.md                # Advanced Usage Guide
├── CHANGELOG.md               # Version History
└── PROJECT_STRUCTURE.md       # This file
```

---

## Module Responsibilities

### desksorter_premium.py
**Main GUI Application** (~1100 lines)

**Responsibilities:**
- User interface with tabbed interface (6 tabs)
- Event handling and user interactions
- Threading for non-blocking operations
- Status updates and logging

**Main Class:**
```python
class DeskSorterPremium:
    def __init__(self, root)
    def setup_menu_bar()
    def setup_notebook()              # Tab setup
    def setup_organize_tab()          # Tab 1
    def setup_rules_tab()             # Tab 2
    def setup_automation_tab()        # Tab 3
    def setup_analytics_tab()         # Tab 4
    def setup_advanced_tab()          # Tab 5
    def setup_settings_tab()          # Tab 6
```

**Tabs:**
1. **Organize Files** - Main organizing interface
2. **Custom Rules** - Create/edit profiles and categories
3. **Automation** - Scheduling and batch processing
4. **Analytics** - Statistics and reports
5. **Advanced** - Duplicate detection and smart naming
6. **Settings** - User preferences and appearance

---

### sorter_engine.py
**Core Sorting Engine** (~300 lines)

**Responsibilities:**
- File organization logic
- Duplicate detection
- Move operations
- History tracking
- Statistics queries

**Main Class:**
```python
class SortingEngine:
    def organize_folder()             # Main method
    def _process_file()               # File processor
    def _apply_smart_naming()         # Naming logic
    def find_duplicates()             # Duplicate detection
    def undo_move()                   # Undo operations
    def add_to_history()              # DB operations
    def get_statistics()              # Analytics
```

**Features:**
- Non-blocking file processing
- Multiple file matching
- Smart file naming
- MD5 hash-based duplication
- SQLite integration
- Thread-safe operations

---

### config_manager.py
**Configuration Manager** (~150 lines)

**Responsibilities:**
- Load/save configuration
- Profile management
- Settings validation
- Default configurations

**Main Class:**
```python
class ConfigManager:
    def load()                        # Load from JSON
    def save()                        # Save to JSON
    def get_profile()                 # Retrieve profile
    def create_profile()              # New profile
    def delete_profile()              # Remove profile
    def update_profile_categories()   # Modify categories
```

**Managed Data:**
- Profiles (multiple sorting configurations)
- User preferences
- Scheduled tasks
- Application state

---

### utils.py
**Utility Functions** (~350 lines)

**Modules:**

1. **FileUtils**
   - `get_file_hash()` - MD5/SHA hashing
   - `get_file_size_human()` - Format file sizes
   - `get_file_info()` - Comprehensive file data
   - `is_file_in_use()` - Check file availability
   - `safe_filename()` - Sanitize filenames

2. **DateUtils**
   - `get_today()` - Current date
   - `format_datetime()` - Format dates
   - `get_file_date()` - File modification time

3. **ReportGenerator**
   - `generate_csv_report()` - Export CSV
   - `generate_json_report()` - Export JSON
   - `generate_text_report()` - Export text

4. **ValidationUtils**
   - `is_valid_path()` - Verify folder path
   - `is_valid_extension()` - Check extension format
   - `is_valid_time_format()` - Validate HH:MM
   - `is_safe_folder_name()` - Check folder name

5. **SystemUtils**
   - `get_os_name()` - Operating system info
   - `get_python_version()` - Python version
   - `get_disk_space()` - Available disk space

---

## Data Flow

### File Organization Flow
```
User Input
    ↓
Validate Folder & Settings
    ↓
Load Profile & Categories
    ↓
Get File List (with filters)
    ↓
For Each File:
    ├─ Detect Category (by extension)
    ├─ Check Duplicates (if enabled)
    ├─ Apply Smart Naming (if enabled)
    └─ Move File (or preview in dry run)
    ↓
Update Database
    ↓
Update Statistics
    ↓
Log Results
```

### Configuration Flow
```
config.json
    ↓
ConfigManager.load()
    ↓
Application Memory
    ↓
User Changes
    ↓
ConfigManager.save()
    ↓
config.json
```

### History & Analytics Flow
```
File Move Operation
    ↓
SortingEngine.add_to_history()
    ↓
SQLite Database (desksorter.db)
    ↓
SortingEngine.get_statistics()
    ↓
Analytics Tab Display
    ↓
Export (CSV/JSON)
```

---

## Database Schema

### move_history Table
```sql
CREATE TABLE move_history (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,           -- ISO format datetime
    filename TEXT,            -- Original filename
    source_path TEXT,        -- Full source path
    dest_path TEXT,          -- Full destination path
    category TEXT,           -- Assigned category
    profile_name TEXT        -- Profile used
);
```

### file_hashes Table
```sql
CREATE TABLE file_hashes (
    id INTEGER PRIMARY KEY,
    filepath TEXT,           -- Full file path
    file_hash TEXT,         -- MD5 hash
    file_size INTEGER,      -- File size in bytes
    last_modified TEXT      -- Last modification time
);
```

---

## Configuration Schema (config.json)

```json
{
  "profiles": {
    "ProfileName": {
      "categories": {
        "CategoryName": [".ext1", ".ext2"]
      },
      "settings": {
        "create_subfolder": boolean,
        "smart_naming": boolean,
        "skip_duplicates": boolean,
        "include_subfolders": boolean
      }
    }
  },
  "last_path": "string",
  "dark_mode": boolean,
  "auto_start": boolean,
  "confirm_deletion": boolean,
  "scheduled_tasks": [...]
}
```

---

## Class Hierarchy

```
DeskSorterPremium (GUI)
├── Uses SortingEngine (Logic)
├── Uses ConfigManager (Config)
└── Uses utils (Helpers)

SortingEngine
└── Interacts with SQLite (desksorter.db)

ConfigManager
└── Interacts with JSON (config.json)

Utility Classes
└── FileUtils, DateUtils, ReportGenerator, etc.
```

---

## Threading Model

### Main Thread (UI Thread)
- Handles all GUI updates
- Processes user inputs
- Updates logs and status

### Worker Threads
1. **Organization Thread**
   - Runs `start_organize()` in background
   - Non-blocking file operations
   - Updates main thread via GUI methods

2. **Watch Folder Thread**
   - Monitors directory for changes
   - Checks at configurable intervals
   - Auto-organizes new files

3. **Batch Processing Thread**
   - Processes multiple folders
   - Sequential processing (one after another)
   - Reports progress

---

## Key Features Implementation

### 1. Undo/Redo System
- **Implementation**: List-based history stacks
- **Files**: Main app (`undo_history`, `redo_history`)
- **Limitation**: Per-session only (not persisted)

### 2. Duplicate Detection
- **Algorithm**: MD5 hash comparison
- **Performance**: ~1-2ms per file
- **Storage**: `file_hashes` table in database

### 3. Smart Naming
- **Pattern**: `{name}_{date}_{hash}_{size}`
- **Supported Variables**:
  - `{name}` - Filename
  - `{date}` - YYYYMMDD format
  - `{hash}` - First 8 chars of MD5
  - `{size}` - File size in bytes

### 4. Profile System
- **Storage**: JSON config file
- **Flexibility**: Unlimited custom profiles
- **Features**: Category customization, settings per profile

### 5. Scheduling
- **Library**: `schedule` module
- **Implementation**: Background thread
- **Frequencies**: Daily, Weekly, Monthly

### 6. Batch Processing
- **Method**: Sequential folder processing
- **Queue**: Listbox-based queue UI
- **Threading**: Single worker thread

### 7. Analytics
- **Storage**: SQLite database
- **Queries**: Aggregation by category and profile
- **Export**: CSV and JSON formats

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| tkinter | built-in | GUI framework |
| sqlite3 | built-in | Database |
| json | built-in | Configuration |
| pathlib | built-in | Path handling |
| hashlib | built-in | File hashing |
| shutil | built-in | File operations |
| threading | built-in | Concurrency |
| Pillow | 9.5.0 | Image handling (optional) |
| send2trash | 1.8.16 | Safe file deletion |
| schedule | 1.1.9 | Task scheduling |

---

## Performance Characteristics

| Operation | Time (approx) | Scalability |
|-----------|---------------|------------|
| Organize 100 files | 1-2 seconds | Linear |
| Organize 1,000 files | 10-20 seconds | Linear |
| Scan for duplicates (100 files) | 1-2 seconds | O(n) |
| Scan for duplicates (10,000 files) | 30-60 seconds | O(n) |
| Database query (1000 records) | <100ms | Indexed |

---

## Security Considerations

1. **File Access**
   - Uses standard `shutil.move()` for reliability
   - Respects OS file permissions
   - Validates paths before operations

2. **Data Privacy**
   - All operations local (no cloud/internet)
   - Database stored locally
   - No external data collection

3. **Error Handling**
   - Graceful error recovery
   - User-friendly error messages
   - Detailed logging for debugging

---

## Future Architecture Improvements

1. **Plugin System**
   - Load custom sorters dynamically
   - Allow custom category detection

2. **Cloud Integration**
   - Abstract file operations interface
   - Support OneDrive, Google Drive, etc.

3. **Async/Await**
   - Replace threading with asyncio
   - Better error handling and cancellation

4. **Web Interface**
   - REST API backend
   - Web UI for remote access
   - Mobile app support

5. **Machine Learning**
   - Auto-detect categories
   - Pattern learning
   - Predictive organization

---

## Code Quality

- **Style**: PEP 8 compliant
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Try-except blocks for robustness
- **Testing**: Unit tests recommended for modules
- **Maintainability**: Modular design, separation of concerns

---

## Deployment & Distribution

### Single-File Version
Could combine all modules into `desksorter.py` for distribution

### Packaged Version
- `setup.py` for PyPI distribution
- Wheel package (.whl) for easy installation
- Windows installer (.exe) with PyInstaller

### Containerized
- Docker image for consistent environment
- Compose file for automated setup

---

*DeskSorter Premium - Professional Architecture Documentation*
