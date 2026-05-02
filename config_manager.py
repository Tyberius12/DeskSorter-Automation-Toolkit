"""
DeskSorter Configuration Manager
Handles loading, saving, and validation of configuration
"""

import json
from pathlib import Path

class ConfigManager:
    """Manages DeskSorter configuration"""
    
    DEFAULT_CONFIG = {
        "profiles": {
            "Default": {
                "categories": {
                    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
                    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.pptx', '.csv'],
                    "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm'],
                    "Music": ['.mp3', '.wav', '.flac', '.aac', '.m4a'],
                    "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz'],
                    "Others": []
                },
                "settings": {
                    "create_subfolder": False,
                    "smart_naming": False,
                    "skip_duplicates": False,
                    "include_subfolders": False
                }
            }
        },
        "last_path": "",
        "dark_mode": False,
        "auto_start": False,
        "confirm_deletion": True,
        "scheduled_tasks": []
    }
    
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.config = self.load()
    
    def load(self):
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get config value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set config value"""
        self.config[key] = value
        return self.save()
    
    def get_profile(self, profile_name):
        """Get a specific profile"""
        return self.config.get("profiles", {}).get(profile_name)
    
    def create_profile(self, profile_name, base_profile="Default"):
        """Create new profile from base"""
        if profile_name in self.config["profiles"]:
            return False
        
        base = self.config["profiles"].get(base_profile, self.DEFAULT_CONFIG["profiles"]["Default"])
        self.config["profiles"][profile_name] = base.copy()
        return self.save()
    
    def delete_profile(self, profile_name):
        """Delete a profile"""
        if profile_name == "Default":
            return False
        
        if profile_name in self.config["profiles"]:
            del self.config["profiles"][profile_name]
            return self.save()
        return False
    
    def update_profile_categories(self, profile_name, categories):
        """Update categories for a profile"""
        if profile_name in self.config["profiles"]:
            self.config["profiles"][profile_name]["categories"] = categories
            return self.save()
        return False
    
    def reset_to_default(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save()
