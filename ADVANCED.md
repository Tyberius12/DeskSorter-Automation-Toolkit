# Advanced Usage Guide - DeskSorter Premium

This guide covers advanced features and programmatic usage of DeskSorter.

## Using DeskSorter Modules Programmatically

### Using the Sorting Engine

```python
from sorter_engine import SortingEngine

# Initialize engine
engine = SortingEngine()

# Define categories
categories = {
    "Images": ['.jpg', '.png', '.gif'],
    "Documents": ['.pdf', '.doc', '.docx'],
    "Videos": ['.mp4', '.avi']
}

# Organize folder
result = engine.organize_folder(
    source_path="/path/to/folder",
    categories=categories,
    options={
        "dry_run": True,
        "include_subfolders": False,
        "smart_naming": False,
        "skip_duplicates": False
    }
)

# Check results
print(f"Moved: {result['moved']} files")
print(f"Skipped: {result['skipped']} files")
print(f"Errors: {result['errors']} files")

# Get moved files details
for file_info in result['moved_files']:
    print(f"  {file_info['file']} -> {file_info['category']}")
```

### Using the Configuration Manager

```python
from config_manager import ConfigManager

# Initialize config manager
config = ConfigManager("config.json")

# Get configuration
profiles = config.get("profiles")
last_path = config.get("last_path")

# Create new profile
config.create_profile("MyProfile", base_profile="Default")

# Get profile
profile = config.get_profile("MyProfile")
print(profile["categories"])

# Update profile
categories = profile["categories"]
categories["Code"] = ['.py', '.js', '.java']
config.update_profile_categories("MyProfile", categories)

# Save all changes
config.save()
```

### Using Utility Functions

```python
from utils import FileUtils, ValidationUtils, ReportGenerator

# Get file hash
file_hash = FileUtils.get_file_hash("path/to/file.txt")
print(f"MD5: {file_hash}")

# Get file info
info = FileUtils.get_file_info("path/to/file.txt")
print(f"Size: {info['size_human']}")
print(f"Modified: {info['modified']}")

# Validate path
if ValidationUtils.is_valid_path("/path/to/folder"):
    print("Valid folder path!")

# Generate report
records = [
    {"file": "document.pdf", "category": "Documents"},
    {"file": "photo.jpg", "category": "Images"}
]
ReportGenerator.generate_csv_report("report.csv", records)
```

---

## Advanced Workflows

### Custom Batch Processing Script

```python
from pathlib import Path
from sorter_engine import SortingEngine
from config_manager import ConfigManager

def batch_organize(folders_list, profile_name):
    """Organize multiple folders using same profile"""
    config = ConfigManager()
    profile = config.get_profile(profile_name)
    categories = profile["categories"]
    
    engine = SortingEngine()
    results = []
    
    for folder in folders_list:
        print(f"\nProcessing {folder}...")
        result = engine.organize_folder(
            source_path=folder,
            categories=categories,
            options={
                "dry_run": False,
                "include_subfolders": True,
                "smart_naming": True,
                "skip_duplicates": True
            }
        )
        results.append({
            "folder": folder,
            "moved": result['moved'],
            "errors": result['errors']
        })
        print(f"  Moved: {result['moved']}, Errors: {result['errors']}")
    
    return results

# Usage
folders = [
    "/Users/Downloads",
    "/Users/Pictures",
    "/Users/Documents"
]
batch_organize(folders, "Default")
```

### Smart Duplicate Cleanup

```python
from sorter_engine import SortingEngine
from pathlib import Path

def cleanup_duplicates(folder, delete=False):
    """Find and optionally delete duplicates"""
    engine = SortingEngine()
    duplicates = engine.find_duplicates(folder)
    
    for file_hash, files in duplicates.items():
        print(f"\nDuplicate group ({file_hash}):")
        
        # Keep first, flag others for deletion
        keep_file = files[0]
        delete_files = files[1:]
        
        print(f"  Keep: {keep_file}")
        for f in delete_files:
            print(f"  Delete: {f}")
            
            if delete:
                try:
                    Path(f).unlink()
                    print(f"    ✓ Deleted")
                except Exception as e:
                    print(f"    ✗ Error: {e}")

# Usage
cleanup_duplicates("/Users/Downloads", delete=False)  # Preview
cleanup_duplicates("/Users/Downloads", delete=True)   # Actually delete
```

### Custom File Organization Rules

```python
from sorter_engine import SortingEngine
from pathlib import Path
import json

def organize_by_date(folder_path):
    """Organize files by year/month"""
    engine = SortingEngine()
    
    for file_path in Path(folder_path).iterdir():
        if file_path.is_file():
            # Get file date
            from datetime import datetime
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            # Create year/month structure
            year_month = mod_time.strftime("%Y/%B")  # 2026/May
            dest_folder = Path(folder_path) / year_month
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            # Move file
            dest_path = dest_folder / file_path.name
            file_path.rename(dest_path)
            print(f"Moved {file_path.name} to {year_month}/")

# Usage
organize_by_date("/Users/Documents")
```

---

## Configuration Customization

### Creating Complex Profile Structures

```python
from config_manager import ConfigManager

config = ConfigManager()

# Create a complex profile for media organization
media_profile = {
    "categories": {
        "Photos": ['.jpg', '.jpeg', '.png', '.raw', '.heic'],
        "Videos": ['.mp4', '.mkv', '.mov', '.avi'],
        "Music": ['.mp3', '.flac', '.wav', '.aac'],
        "Edited": ['.psd', '.ai', '.ae'],
        "Projects": ['.prproj', '.fcpxml']
    },
    "settings": {
        "create_subfolder": True,
        "smart_naming": True,
        "skip_duplicates": True,
        "include_subfolders": True
    }
}

# Save to config
config.config["profiles"]["MediaOrganization"] = media_profile
config.save()
```

### Profile-based Automation

```python
import schedule
import time
from sorter_engine import SortingEngine
from config_manager import ConfigManager

def scheduled_organize():
    """Run organization on schedule"""
    config = ConfigManager()
    path = config.get("last_path")
    profile = config.get_profile("Default")
    
    if not path:
        print("No path configured!")
        return
    
    engine = SortingEngine()
    result = engine.organize_folder(
        source_path=path,
        categories=profile["categories"],
        options={"dry_run": False}
    )
    
    print(f"Scheduled organization: {result['moved']} files moved")

# Schedule daily at 9:00 AM
schedule.every().day.at("09:00").do(scheduled_organize)

# Run scheduler (in background)
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Advanced Filtering & Processing

### Organization by File Size

```python
from pathlib import Path

def organize_by_size(folder, size_categories):
    """
    Organize files by size ranges.
    
    size_categories = {
        "Small": (0, 1024*1024),           # 0-1MB
        "Medium": (1024*1024, 100*1024*1024),  # 1-100MB
        "Large": (100*1024*1024, float('inf'))  # 100MB+
    }
    """
    for file_path in Path(folder).iterdir():
        if file_path.is_file():
            size = file_path.stat().st_size
            
            for category, (min_size, max_size) in size_categories.items():
                if min_size <= size < max_size:
                    dest_folder = Path(folder) / category
                    dest_folder.mkdir(exist_ok=True)
                    file_path.rename(dest_folder / file_path.name)
                    print(f"Moved {file_path.name} to {category}")
                    break

# Usage
sizes = {
    "Small": (0, 1024*1024),
    "Medium": (1024*1024, 100*1024*1024),
    "Large": (100*1024*1024, float('inf'))
}
organize_by_size("/Users/Downloads", sizes)
```

### Advanced File Filtering

```python
from pathlib import Path
import re

def organize_with_patterns(folder, patterns):
    """
    Organize files using regex patterns.
    
    patterns = {
        "Screenshots": r"Screenshot_\d+",
        "Backups": r".*\.backup",
        "Logs": r".*\.log$"
    }
    """
    for file_path in Path(folder).iterdir():
        if file_path.is_file():
            filename = file_path.name
            
            for category, pattern in patterns.items():
                if re.match(pattern, filename):
                    dest_folder = Path(folder) / category
                    dest_folder.mkdir(exist_ok=True)
                    file_path.rename(dest_folder / file_path.name)
                    print(f"Moved {filename} to {category}")
                    break

# Usage
patterns = {
    "Screenshots": r"Screenshot",
    "Backups": r".*\.backup",
    "Archives": r".*\.zip|.*\.rar"
}
organize_with_patterns("/Users/Downloads", patterns)
```

---

## Monitoring & Statistics

### Build Custom Statistics

```python
from sorter_engine import SortingEngine
import json

def get_organization_stats():
    """Get detailed organization statistics"""
    engine = SortingEngine()
    stats = engine.get_statistics()
    
    print("=== Organization Statistics ===\n")
    print(f"Total Moves: {stats['total_moves']}")
    
    print("\nBy Category:")
    for category, count in stats['by_category']:
        print(f"  {category}: {count}")
    
    print("\nBy Profile:")
    for profile, count in stats['by_profile']:
        print(f"  {profile}: {count}")
    
    print("\nRecent Moves:")
    for filename, category, timestamp in stats['recent_moves'][:5]:
        print(f"  {filename} -> {category} ({timestamp})")
    
    return stats

# Usage
stats = get_organization_stats()
```

### Generate Organization Report

```python
from sorter_engine import SortingEngine
from utils import ReportGenerator
from datetime import datetime

def generate_organization_report(output_file="report.json"):
    """Generate comprehensive organization report"""
    engine = SortingEngine()
    stats = engine.get_statistics()
    
    report = {
        "generated": datetime.now().isoformat(),
        "summary": {
            "total_files_organized": stats['total_moves'],
            "categories": dict(stats['by_category']),
            "profiles": dict(stats['by_profile'])
        },
        "recent_operations": [
            {
                "filename": f[0],
                "category": f[1],
                "timestamp": f[2]
            } for f in stats['recent_moves']
        ]
    }
    
    ReportGenerator.generate_json_report(output_file, report)
    print(f"Report generated: {output_file}")

# Usage
generate_organization_report()
```

---

## Error Handling & Recovery

### Safe File Operations with Rollback

```python
from sorter_engine import SortingEngine
from pathlib import Path

def safe_organize_with_rollback(folder, categories, max_errors=5):
    """
    Organize with automatic rollback on too many errors
    """
    engine = SortingEngine()
    move_log = []
    
    result = engine.organize_folder(
        source_path=folder,
        categories=categories,
        options={"dry_run": False}
    )
    
    if result['errors'] > max_errors:
        print(f"Too many errors ({result['errors']}), rolling back...")
        
        # Undo moves
        for move in result['moved_files']:
            engine.undo_move(move['source'], move['destination'])
            print(f"Rolled back: {move['file']}")
        
        return False
    
    return True

# Usage
categories = {"Documents": ['.pdf', '.doc']}
safe_organize_with_rollback("/Users/Downloads", categories)
```

---

## Integration Examples

### With Other Tools

```python
# Integration with system notifications
from sorter_engine import SortingEngine

def organize_and_notify(folder, categories):
    """Organize and send notification"""
    engine = SortingEngine()
    result = engine.organize_folder(folder, categories)
    
    # Send notification (Windows)
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            "DeskSorter",
            f"Organized {result['moved']} files!",
            duration=10
        )
    except:
        pass  # Notification system not available

# Integration with logging
import logging

logging.basicConfig(filename='desksorter.log', level=logging.INFO)

def organize_with_logging(folder, categories):
    engine = SortingEngine()
    result = engine.organize_folder(folder, categories)
    
    logging.info(f"Organization completed: {result['moved']} moved, {result['errors']} errors")
```

---

## Performance Optimization

### Batch Processing Large Folders

```python
from pathlib import Path
from sorter_engine import SortingEngine
import concurrent.futures

def parallel_organize(folder_list, categories, max_workers=3):
    """Process multiple folders in parallel"""
    
    def organize_folder(folder):
        engine = SortingEngine()
        return engine.organize_folder(folder, categories)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(organize_folder, folder_list))
    
    total_moved = sum(r['moved'] for r in results if r['success'])
    print(f"Total files moved: {total_moved}")
    
    return results

# Usage
folders = ["/Users/Downloads", "/Users/Desktop", "/Users/Documents"]
parallel_organize(folders, {"Documents": ['.pdf', '.doc']})
```

---

For more examples and advanced usage, check the source code in:
- `sorter_engine.py` - Core engine implementation
- `config_manager.py` - Configuration management
- `utils.py` - Utility functions

---

*DeskSorter Premium - Advanced Automation Guide*
