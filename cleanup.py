#!/usr/bin/env python
"""
Cleanup script for DocBuddy development.

This script removes build artifacts and temporary files to keep the project directory clean.
Run this after building and uploading packages to PyPI, or whenever you want to clean up.

Usage:
    python cleanup.py [--all]

Options:
    --all: Also remove the .kb directory (knowledge base) and configuration files.
"""

import os
import sys
import glob
import shutil
from pathlib import Path


def print_header(message):
    """Print a header message."""
    print(f"\n{'-' * 80}")
    print(f"{message}")
    print(f"{'-' * 80}")


def remove_path(path, description):
    """Remove a file or directory with description."""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"✓ Removed {description}: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"✓ Removed {description}: {path}")
        else:
            print(f"! Not found: {path}")
    except Exception as e:
        print(f"! Error removing {path}: {e}")


def cleanup(clean_all=False):
    """
    Clean up build artifacts and temporary files.
    
    Args:
        clean_all: Whether to also remove knowledge base and config files.
    """
    # Get project root directory (where this script is located)
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    print_header("Cleaning up DocBuddy project directory")
    print(f"Project root: {project_root}")
    
    # Remove build artifacts
    print_header("Removing build artifacts")
    
    # Remove dist directory
    remove_path("dist", "distribution directory")
    
    # Remove build directory
    remove_path("build", "build directory")
    
    # Remove egg-info directories
    for egg_info in glob.glob("*.egg-info"):
        remove_path(egg_info, "egg-info directory")
    
    # Remove version directories (like docbuddy-0.1.1)
    for version_dir in glob.glob("docbuddy-*.*.*"):
        remove_path(version_dir, "version directory")
        
    # Remove version directories inside docbuddy
    for version_dir in glob.glob("docbuddy/docbuddy-*.*.*"):
        remove_path(version_dir, "version directory")
    
    # Remove wheel files
    for wheel in glob.glob("**/*.whl", recursive=True):
        remove_path(wheel, "wheel file")
        
    # Remove tar.gz files
    for targz in glob.glob("**/*.tar.gz", recursive=True):
        remove_path(targz, "tar.gz file")
    
    # Remove __pycache__ directories
    print_header("Removing Python cache files")
    for pycache in glob.glob("**/__pycache__", recursive=True):
        remove_path(pycache, "Python cache directory")
    
    # Remove .pyc files
    for pyc in glob.glob("**/*.pyc", recursive=True):
        remove_path(pyc, "compiled Python file")
    
    # Remove .pyo files
    for pyo in glob.glob("**/*.pyo", recursive=True):
        remove_path(pyo, "optimized Python file")
    
    # Remove .pyd files
    for pyd in glob.glob("**/*.pyd", recursive=True):
        remove_path(pyd, "Python extension file")
    
    # Remove additional files only if --all is specified
    if clean_all:
        print_header("Removing knowledge base and configuration files")
        
        # Remove .kb directories
        for kb_dir in glob.glob("**/.kb", recursive=True):
            remove_path(kb_dir, "knowledge base directory")
        
        # Remove config.json
        if os.path.exists("config.json"):
            remove_path("config.json", "configuration file")
        
        # Remove .env file
        if os.path.exists(".env"):
            remove_path(".env", "environment variables file")
    
    print_header("Cleanup completed!")
    print("Note: If you've made changes to the code, remember to rebuild the package")
    print("if necessary before distributing or installing.")
    if not clean_all:
        print("\nTip: Run with --all to also remove knowledge base and config files.")


if __name__ == "__main__":
    clean_all = "--all" in sys.argv
    cleanup(clean_all)