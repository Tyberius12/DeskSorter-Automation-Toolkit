"""
DeskSorter Core Sorting Engine
Handles file organization logic independently from UI
"""

import shutil
from pathlib import Path
from datetime import datetime
import hashlib
from collections import defaultdict
import sqlite3

class SortingEngine:
    """Core file sorting logic"""
    
    def __init__(self, db_path="desksorter.db"):
        self.db_path = Path(db_path)
        self.moved_files = []
        self.skipped_files = []
        self.errors = []
    
    def organize_folder(self, source_path, categories, options=None):
        """
        Organize files in a folder according to categories.
        
        Args:
            source_path: Path to organize
            categories: Dict of {category: [extensions]}
            options: Dict with keys:
                - dry_run: bool (default True)
                - include_subfolders: bool (default False)
                - smart_naming: bool (default False)
                - skip_duplicates: bool (default False)
                - naming_pattern: str (default "{name}")
        
        Returns:
            dict with results
        """
        options = options or {}
        p = Path(source_path)
        
        if not p.exists() or not p.is_dir():
            return {
                "success": False,
                "error": "Path does not exist or is not a directory"
            }
        
        self.moved_files = []
        self.skipped_files = []
        self.errors = []
        
        try:
            # Get file list
            if options.get("include_subfolders", False):
                items = list(p.rglob('*'))
            else:
                items = list(p.iterdir())
            
            # Filter to files only
            files = [f for f in items if f.is_file() and not f.name.startswith('.')]
            
            # Process each file
            for file_path in files:
                self._process_file(
                    file_path, p, categories, options
                )
            
            return {
                "success": True,
                "moved": len(self.moved_files),
                "skipped": len(self.skipped_files),
                "errors": len(self.errors),
                "moved_files": self.moved_files,
                "skipped_files": self.skipped_files,
                "error_details": self.errors
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _process_file(self, file_path, root_path, categories, options):
        """Process a single file"""
        ext = file_path.suffix.lower()
        category = "Others"
        
        # Find matching category
        for cat, exts in categories.items():
            if ext in exts:
                category = cat
                break
        
        dest_folder = root_path / category
        dest_path = dest_folder / file_path.name
        
        # Apply smart naming if enabled
        if options.get("smart_naming", False):
            pattern = options.get("naming_pattern", "{name}")
            dest_path = self._apply_smart_naming(file_path, dest_folder, pattern)
        
        # Handle duplicates
        if options.get("skip_duplicates", False) and dest_path.exists():
            self.skipped_files.append({
                "file": file_path.name,
                "reason": "Duplicate exists"
            })
            return
        
        # Perform move
        if options.get("dry_run", True):
            self.moved_files.append({
                "file": file_path.name,
                "source": str(file_path),
                "destination": str(dest_path),
                "category": category,
                "dry_run": True
            })
        else:
            try:
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(dest_path))
                
                self.moved_files.append({
                    "file": file_path.name,
                    "source": str(file_path),
                    "destination": str(dest_path),
                    "category": category,
                    "dry_run": False
                })
            except Exception as e:
                self.errors.append({
                    "file": file_path.name,
                    "error": str(e)
                })
    
    def _apply_smart_naming(self, file_path, dest_folder, pattern):
        """Apply smart naming pattern to file"""
        name = file_path.stem
        ext = file_path.suffix
        
        try:
            mod_time = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).strftime("%Y%m%d")
            size = file_path.stat().st_size
            file_hash = self._get_file_hash(str(file_path))[:8]
            
            new_name = pattern.format(
                name=name, date=mod_time, size=size, hash=file_hash
            )
            return dest_folder / (new_name + ext)
        except:
            return dest_folder / (name + ext)
    
    @staticmethod
    def _get_file_hash(filepath):
        """Get MD5 hash of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return "unknown"
    
    def find_duplicates(self, folder_path):
        """
        Find duplicate files in folder based on content hash.
        
        Returns:
            dict of {hash: [file_paths]}
        """
        p = Path(folder_path)
        hash_dict = defaultdict(list)
        
        for file_path in p.rglob('*'):
            if file_path.is_file():
                file_hash = self._get_file_hash(str(file_path))
                hash_dict[file_hash].append(str(file_path))
        
        # Filter to only duplicates
        duplicates = {
            h: files for h, files in hash_dict.items() 
            if len(files) > 1
        }
        
        return duplicates
    
    def undo_move(self, source, destination):
        """Undo a file move operation"""
        try:
            shutil.move(destination, source)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_to_history(self, filename, source, destination, category, profile):
        """Add move operation to database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            timestamp = datetime.now().isoformat()
            
            c.execute('''
                INSERT INTO move_history 
                (timestamp, filename, source_path, dest_path, category, profile_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, filename, source, destination, category, profile))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def get_statistics(self):
        """Get organization statistics from database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            
            # Total moves
            c.execute("SELECT COUNT(*) FROM move_history")
            total = c.fetchone()[0]
            
            # By category
            c.execute("""
                SELECT category, COUNT(*) FROM move_history 
                GROUP BY category ORDER BY COUNT(*) DESC
            """)
            by_category = c.fetchall()
            
            # By profile
            c.execute("""
                SELECT profile_name, COUNT(*) FROM move_history 
                GROUP BY profile_name ORDER BY COUNT(*) DESC
            """)
            by_profile = c.fetchall()
            
            # Recent moves
            c.execute("""
                SELECT filename, category, timestamp FROM move_history 
                ORDER BY timestamp DESC LIMIT 10
            """)
            recent = c.fetchall()
            
            conn.close()
            
            return {
                "total_moves": total,
                "by_category": by_category,
                "by_profile": by_profile,
                "recent_moves": recent
            }
        except Exception as e:
            return {"error": str(e)}
