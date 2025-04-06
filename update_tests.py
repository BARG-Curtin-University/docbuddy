#!/usr/bin/env python3
"""
Script to update imports in test files.
"""
import glob
import os
from pathlib import Path

# Find all test files
test_files = glob.glob('/home/michael/Projects/github-repos/projects/doc-buddy/docbuddy/tests/*.py')

for file_path in test_files:
    # Skip test_basic.py as we've already updated it
    if os.path.basename(file_path) == 'test_basic.py':
        continue
        
    # Read the content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace imports
    updated_content = content.replace('from docbuddy', 'from ask_docs')
    updated_content = updated_content.replace('import docbuddy', 'import ask_docs')
    updated_content = updated_content.replace('docbuddy.', 'ask_docs.')
    
    # Replace DocBuddy in docstrings and comments
    updated_content = updated_content.replace('DocBuddy', 'AskDocs')
    
    # Write the updated content
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path}")

print("Tests update complete!")