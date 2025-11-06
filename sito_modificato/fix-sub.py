#!/usr/bin/env python3
"""Fix search.js paths in subcategories"""
import os
from pathlib import Path

base_dir = Path(".")

# Fix subcategories
subcategories_dir = base_dir / "subcategories"
if subcategories_dir.exists():
    for file in subcategories_dir.glob("*.html"):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix search.js path
        content = content.replace('src="search.js"', 'src="https://calcdomain.com/search.js"')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {file.name}")

print("Paths fixed in subcategories")
