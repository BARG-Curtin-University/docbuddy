#!/usr/bin/env python3
"""
Script to update references to 'DocBuddy' in template files.
"""
import glob
import os
from pathlib import Path

# Update all HTML files in templates directory
template_files = glob.glob('/home/michael/Projects/github-repos/projects/doc-buddy/docbuddy/ask_docs/web/templates/*.html')

for file_path in template_files:
    # Read the content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace DocBuddy with AskDocs
    updated_content = content.replace('DocBuddy', 'AskDocs')
    
    # Write the updated content
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path}")

# Update TUI CSS files
css_files = glob.glob('/home/michael/Projects/github-repos/projects/doc-buddy/docbuddy/ask_docs/tui/*.css')

for file_path in css_files:
    # Read the content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace DocBuddy with AskDocs
    updated_content = content.replace('DocBuddy', 'AskDocs')
    
    # Write the updated content
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path}")

# Update documentation files
doc_files = glob.glob('/home/michael/Projects/github-repos/projects/doc-buddy/docbuddy/docs/interfaces/*.md')

for file_path in doc_files:
    # Read the content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace DocBuddy with AskDocs and docbuddy with askdocs
    updated_content = content.replace('DocBuddy', 'AskDocs')
    updated_content = updated_content.replace('docbuddy', 'askdocs')
    updated_content = updated_content.replace('from docbuddy', 'from ask_docs')
    updated_content = updated_content.replace('import docbuddy', 'import ask_docs')
    
    # Write the updated content
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path}")

print("Template update complete!")