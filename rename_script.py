#!/usr/bin/env python3
"""
Script to rename docbuddy to ask_docs in all Python files.
"""
import os
import shutil
import re
from pathlib import Path

def process_file(source_path, target_path):
    # Create parent directories if they don't exist
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy the file
    if source_path.name.endswith('.py'):
        # For Python files, replace imports and docstrings
        with open(source_path, 'r') as f:
            content = f.read()
        
        # Replace imports and module references
        content = content.replace('from docbuddy', 'from ask_docs')
        content = content.replace('import docbuddy', 'import ask_docs')
        content = content.replace('docbuddy.', 'ask_docs.')
        
        # Replace DocBuddy in docstrings and comments
        content = content.replace('DocBuddy', 'AskDocs')
        
        with open(target_path, 'w') as f:
            f.write(content)
    else:
        # For non-Python files, just copy
        shutil.copy2(source_path, target_path)

def copy_directory(source_dir, target_dir):
    # Process all files in the directory
    for item in os.listdir(source_dir):
        source_path = source_dir / item
        if source_path.is_dir():
            # Skip __pycache__ directories
            if item == '__pycache__':
                continue
            # For subdirectories, recursively process
            target_subdir = target_dir / item
            copy_directory(source_path, target_subdir)
        else:
            # Process file
            target_path = target_dir / item
            process_file(source_path, target_path)

# Define source and target directories
source_base = Path('/home/michael/Projects/github-repos/projects/doc-buddy/docbuddy/docbuddy')
target_base = Path('/home/michael/Projects/github-repos/projects/doc-buddy/docbuddy/ask_docs')

# Copy all files with renaming
copy_directory(source_base, target_base)

print("Renaming complete!")