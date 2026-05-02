#!/usr/bin/env python3
"""
DeskSorter Premium Setup & Launcher
Handles dependency installation and application startup
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Verify Python version is 3.7+"""
    if sys.version_info < (3, 7):
        print(f"ERROR: Python 3.7+ required. You have {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required packages from requirements.txt"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("ERROR: requirements.txt not found!")
        return False
    
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", str(requirements_file), "--quiet"
        ])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        print("Try running: pip install -r requirements.txt")
        return False

def start_application():
    """Launch the DeskSorter Premium application"""
    app_file = Path("desksorter_premium.py")
    
    if not app_file.exists():
        print("ERROR: desksorter_premium.py not found!")
        return False
    
    print("\n" + "="*40)
    print("  DeskSorter Premium v2.0")
    print("="*40 + "\n")
    
    try:
        subprocess.run([sys.executable, str(app_file)])
        return True
    except Exception as e:
        print(f"ERROR: Failed to start application: {e}")
        return False

def main():
    """Main launcher function"""
    print("\n" + "="*50)
    print("  DeskSorter Premium - Launcher")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        print(f"Current Python version: {sys.version}")
        input("\nPress Enter to exit...")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        input("\nPress Enter to exit...")
        return 1
    
    # Start application
    if not start_application():
        input("\nPress Enter to exit...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
