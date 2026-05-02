# DeskSorter Premium v2.0

A professional file organization utility with advanced features for automatic file sorting and management.

## Features

### ✨ Core Features
- **Automatic File Organization** - Sort files into categories based on file extensions
- **Custom Sorting Rules** - Create unlimited custom categories and file type associations
- **Profile System** - Save multiple sorting profiles for different use cases
- **Dry Run Mode** - Preview changes before applying them

### 🎯 Smart Organization
- **Smart Naming** - Auto-rename files with patterns (date, size, hash)
- **Duplicate Detection** - Find and manage duplicate files with hash comparison
- **Nested Categories** - Organize files into subcategories
- **Skip Duplicates** - Automatically skip existing files in destination

### ⏰ Automation
- **Scheduled Tasks** - Auto-organize folders on daily/weekly/monthly basis
- **Watch Folder Mode** - Monitor folders for new files and organize automatically
- **Batch Processing** - Process multiple folders at once

### 📊 Analytics & Reporting
- **Organization Statistics** - View detailed statistics by category and profile
- **Move History** - Complete database of all file movements
- **Export Reports** - Export statistics as CSV or JSON

### 🎨 Enhanced UX
- **Dark Mode** - Professional dark theme option
- **Undo/Redo System** - Reverse file movements with Ctrl+Z / Ctrl+Y
- **Activity Log** - Real-time logging of all operations
- **Intuitive Interface** - Tabbed interface with organized settings

## Installation

### Requirements
- Python 3.7+
- Windows/macOS/Linux

### Setup Steps

1. **Clone or Download** the DeskSorter folder

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
python desksorter_premium.py
```

## Usage Guide

### Basic Workflow

1. **Select Target Folder** - Click "Browse" to choose the folder to organize
2. **Choose Profile** - Select a pre-configured profile or create a custom one
3. **Configure Options**:
   - ✓ Dry Run (preview mode)
   - ✓ Include Subfolders
   - ✓ Smart Naming
   - ✓ Skip Duplicates
4. **Click "START ORGANIZING"**

### Creating Custom Profiles

1. Go to **Custom Rules** tab
2. Enter a **Profile Name** and click **Create Profile**
3. Add custom categories with file extensions
4. Save and use in the Organize tab

### Automation Setup

1. Go to **Automation** tab
2. **Scheduling**:
   - Enable scheduling
   - Set time (HH:MM format)
   - Choose frequency (Daily/Weekly/Monthly)
3. **Watch Mode**:
   - Enable watch mode for automatic detection of new files
   - Set check interval in seconds
4. **Batch Processing**:
   - Add multiple folders
   - Click "Process All"

### Finding & Managing Duplicates

1. Go to **Advanced** tab
2. Click **Scan for Duplicates**
3. Review found duplicates
4. Select duplicate files and:
   - Delete permanently
   - Move to Trash
5. Use smart rename patterns to avoid future duplicates

### Viewing Analytics

1. Go to **Analytics** tab
2. Click **Refresh Statistics**
3. View organization history and statistics
4. Export reports as:
   - CSV (spreadsheet format)
   - JSON (data format)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo last file move |
| Ctrl+Y | Redo last action |

## Configuration

The app stores configuration in `config.json`:

```json
{
  "profiles": {
    "ProfileName": {
      "categories": {
        "CategoryName": [".ext1", ".ext2"]
      },
      "settings": { ... }
    }
  },
  "dark_mode": false,
  "auto_start": false
}
```

## Database

- **desksorter.db** - SQLite database storing:
  - Move history with timestamps
  - File hash information for duplicate detection
  - Organization statistics

## Pre-configured Profiles

### Default
Standard profile with common file categories:
- Images, Documents, Videos, Music, Archives, Others

### Photos
Specialized for photo organization:
- By Year, Screenshots, Videos
- Smart naming enabled by default
- Duplicate detection enabled

### Downloads
Optimized for Downloads folder:
- Separates applications, documents, media, archives
- Handles both file types and applications

## Advanced Features

### Smart Naming Pattern
Available variables:
- `{name}` - Original filename
- `{date}` - File modification date (YYYYMMDD)
- `{size}` - File size in bytes
- `{hash}` - First 8 characters of MD5 hash

Example: `{name}_{date}_{hash}`

### File Deduplication
Uses MD5 hash comparison to identify duplicate files based on content, not just filename.

## Troubleshooting

### Permission Denied Errors
- Run with administrator privileges
- Ensure files are not in use by other applications
- Check folder write permissions

### Database Errors
- Delete `desksorter.db` to reset (loses history)
- Ensure disk space available
- Check file system permissions

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Undo/Redo System

All file moves are tracked and can be reversed:
1. **Undo** - Returns files to original location
2. **Redo** - Re-applies undone moves
3. History maintained per session

## Performance Notes

- Scanning large folders may take time (100K+ files)
- Duplicate detection uses MD5 hashing (slower for large files)
- Watch mode checks folder every N seconds
- Database queries optimized for quick lookups

## Support & Feedback

For issues or feature requests, check the activity log for detailed error messages.

## License

DeskSorter Premium - Educational & Personal Use

---

**Version 2.0** - 2026
Built with Python & Tkinter
