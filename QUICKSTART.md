# Quick Start Guide - DeskSorter Premium

## 🚀 Getting Started in 5 Minutes

### Step 1: Install & Launch
**Windows Users:**
```bash
# Double-click launch.bat
# Or run in terminal:
launch.bat
```

**Mac/Linux Users:**
```bash
# Run launcher script:
python3 launch.py

# Or manually:
pip install -r requirements.txt
python3 desksorter_premium.py
```

### Step 2: Select Your Folder
1. Open the **"Organize Files"** tab
2. Click the **"Browse"** button
3. Select the folder you want to organize (e.g., Downloads folder)

### Step 3: Choose a Profile
Select from pre-made profiles:
- **Default** - General purpose organization
- **Photos** - Optimized for photo folders
- **Downloads** - For Downloads folder

Or create your own in the **"Custom Rules"** tab!

### Step 4: Preview Changes (Dry Run)
✓ Keep "Dry Run" **checked** (default)
This shows you what WOULD happen without actually moving files

### Step 5: Start Organizing
Click **"START ORGANIZING"** button

Watch the log to see what's happening!

---

## 💡 Common Workflows

### Organizing Downloads Folder
1. Select Downloads folder
2. Choose **"Downloads"** profile
3. Enable dry run to preview
4. Check the log
5. Uncheck dry run and run again to apply

### Organizing Photo Library
1. Select photo folder
2. Choose **"Photos"** profile
3. Enable "Smart Naming" for better file names
4. Enable "Skip Duplicates" to avoid moving duplicates
5. Run organization

### Batch Processing Multiple Folders
1. Go to **"Automation"** tab
2. In **"Batch Processing"** section:
   - Click "Add Folder" for each folder
   - Click "Process All"

---

## 🎯 Tips & Tricks

### Create Custom Category
1. Go to **"Custom Rules"** tab
2. In **"Edit Categories"** section:
   - Category Name: e.g., "Source Code"
   - Extensions: `.py, .js, .java, .cpp`
3. Click "Add Category"

### Find Duplicate Files
1. Go to **"Advanced"** tab
2. Click "Scan for Duplicates"
3. Review duplicates found
4. Delete or move to trash

### Undo Mistakes
Press **Ctrl+Z** to undo last file move
Press **Ctrl+Y** to redo

### View Statistics
1. Go to **"Analytics"** tab
2. Click "Refresh Statistics"
3. View your organization history
4. Export as CSV or JSON

### Enable Automatic Organization
1. Go to **"Automation"** tab
2. **Scheduling:**
   - Check "Enable Scheduling"
   - Set time (e.g., 09:00)
   - Choose frequency
   - Click "Save Schedule"

---

## ⚙️ Customization Tips

### Create "Work" Profile
1. Go to **"Custom Rules"**
2. Enter profile name: "Work"
3. Click "Create Profile"
4. Add categories for your work files:
   - "Spreadsheets": `.xlsx, .xls, .csv`
   - "Presentations": `.pptx, .ppt`
   - "Reports": `.pdf, .docx`

### Smart File Naming
Enable in organize tab to auto-rename files with:
- **{name}** - Original filename
- **{date}** - Modification date
- **{size}** - File size
- **{hash}** - File hash

Example: Files would be renamed to `document_20260502_12345a1b`

### Skip Duplicates
Check this option to avoid moving files if they already exist in destination with same name.

---

## 🔧 Troubleshooting

### "Permission Denied" Error
- Run as Administrator (right-click → Run as administrator)
- Close files that might be open
- Check folder permissions

### Files Not Moving in Dry Run
This is normal! Dry Run is preview-only mode.
Uncheck "Dry Run" to actually move files.

### Missing Files After Organization
Check the **Activity Log** for any errors.
Use **Undo (Ctrl+Z)** to restore files.

### Database Error
Delete `desksorter.db` file to reset (loses history but fixes errors).

---

## 📊 Viewing Results

### Activity Log
Shows real-time information as files are organized:
- ✓ SUCCESS: File was moved
- ⚠ SKIPPED: File was skipped (duplicate/error)
- ✗ ERROR: File couldn't be moved

### Statistics
Go to **Analytics** tab to see:
- Total files organized
- Files by category
- Files by profile
- Export options (CSV, JSON)

---

## 🎓 Advanced Features

### Watch Folder Mode
Monitors folder for new files and auto-organizes them:
1. Go to **Automation** tab
2. Enable "Watch Folder Mode"
3. Set check interval (in seconds)
4. Click "Start Watch"

### Undo/Redo System
- **Undo** (Ctrl+Z): Reverse last action
- **Redo** (Ctrl+Y): Re-apply last undone action
- History is maintained per session

### Dark Mode
Go to **Settings** tab and toggle "Dark Mode"
(Applies on next restart)

---

## 📚 File Structure

```
DeskSorter/
├── desksorter_premium.py    # Main application
├── sorter_engine.py          # Core sorting logic
├── config_manager.py         # Config handling
├── utils.py                  # Utility functions
├── config.json              # Your settings & profiles
├── desksorter.db            # History database
├── launch.bat               # Windows launcher
├── launch.py                # Python launcher
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
└── QUICKSTART.md           # This file
```

---

## 🆘 Getting Help

**Check the Activity Log:**
The log provides detailed information about what's happening:
- Timestamps for each action
- File names being processed
- Category assignments
- Any errors encountered

**Review Statistics:**
Go to Analytics tab to see your organization history and statistics.

**Reset to Defaults:**
If something goes wrong, you can:
- Delete `config.json` to reset settings
- Delete `desksorter.db` to reset history

---

## 🎉 What's Next?

- Create custom profiles for different folders
- Enable scheduling for automatic organization
- Use watch mode for continuous organization
- Export reports to track your organization
- Try different naming patterns for files

Enjoy organizing with **DeskSorter Premium!** 🎉

