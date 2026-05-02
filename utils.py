"""
DeskSorter Utility Functions
Common helpers and utilities used across the application
"""

import hashlib
from pathlib import Path
from datetime import datetime
import os
import platform

class FileUtils:
    """File utility functions"""
    
    @staticmethod
    def get_file_hash(filepath, algorithm='md5'):
        """
        Calculate file hash using specified algorithm.
        
        Args:
            filepath: Path to file
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        
        Returns:
            Hash string or None on error
        """
        try:
            hash_obj = hashlib.new(algorithm)
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            print(f"Error calculating hash: {e}")
            return None
    
    @staticmethod
    def get_file_size_human(bytes_size):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    @staticmethod
    def get_file_info(filepath):
        """Get comprehensive file information"""
        p = Path(filepath)
        
        if not p.exists():
            return None
        
        try:
            stat = p.stat()
            return {
                "name": p.name,
                "path": str(p),
                "size": stat.st_size,
                "size_human": FileUtils.get_file_size_human(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime),
                "extension": p.suffix,
                "is_file": p.is_file(),
                "is_dir": p.is_dir()
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    @staticmethod
    def is_file_in_use(filepath):
        """Check if file is currently in use"""
        try:
            if not os.path.exists(filepath):
                return False
            
            if platform.system() == 'Windows':
                import msvcrt
                with open(filepath, 'a+b') as f:
                    try:
                        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                        return False
                    except IOError:
                        return True
            else:
                # Unix-like systems
                f = open(filepath, 'a+b')
                f.close()
                return False
        except:
            return True
    
    @staticmethod
    def safe_filename(filename):
        """Remove or replace invalid characters from filename"""
        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()


class DateUtils:
    """Date and time utility functions"""
    
    @staticmethod
    def get_today():
        """Get today's date"""
        return datetime.now().date()
    
    @staticmethod
    def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
        """Format datetime object"""
        return dt.strftime(format_str)
    
    @staticmethod
    def get_file_date(filepath):
        """Get file modification date"""
        try:
            mod_time = Path(filepath).stat().st_mtime
            return datetime.fromtimestamp(mod_time)
        except:
            return None


class ReportGenerator:
    """Generate reports from organization data"""
    
    @staticmethod
    def generate_csv_report(filename, records):
        """Generate CSV report"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if records:
                    # Write header
                    headers = records[0].keys() if isinstance(records[0], dict) else []
                    f.write(','.join(str(h) for h in headers) + '\n')
                    
                    # Write data
                    for record in records:
                        if isinstance(record, dict):
                            values = [str(v).replace(',', ';') for v in record.values()]
                            f.write(','.join(values) + '\n')
            return True
        except Exception as e:
            print(f"Error generating CSV: {e}")
            return False
    
    @staticmethod
    def generate_json_report(filename, data):
        """Generate JSON report"""
        import json
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error generating JSON: {e}")
            return False
    
    @staticmethod
    def generate_text_report(filename, content):
        """Generate text report"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error generating text report: {e}")
            return False


class ValidationUtils:
    """Validation helper functions"""
    
    @staticmethod
    def is_valid_path(path_str):
        """Check if path string is valid"""
        try:
            p = Path(path_str)
            return p.exists() and p.is_dir()
        except:
            return False
    
    @staticmethod
    def is_valid_extension(ext):
        """Check if extension format is valid"""
        return ext.startswith('.')
    
    @staticmethod
    def is_valid_time_format(time_str):
        """Validate HH:MM time format"""
        try:
            parts = time_str.split(':')
            h, m = int(parts[0]), int(parts[1])
            return 0 <= h < 24 and 0 <= m < 60
        except:
            return False
    
    @staticmethod
    def is_safe_folder_name(name):
        """Check if folder name is safe"""
        invalid_chars = r'<>:"/\|?*'
        return not any(char in name for char in invalid_chars)


class SystemUtils:
    """System and environment utilities"""
    
    @staticmethod
    def get_os_name():
        """Get operating system name"""
        return platform.system()
    
    @staticmethod
    def get_python_version():
        """Get Python version"""
        return f"{platform.python_version()}"
    
    @staticmethod
    def get_disk_space(path):
        """Get available disk space for path"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(path)
            return {
                "total": FileUtils.get_file_size_human(total),
                "used": FileUtils.get_file_size_human(used),
                "free": FileUtils.get_file_size_human(free),
                "percent_used": (used / total) * 100
            }
        except Exception as e:
            print(f"Error getting disk space: {e}")
            return None
