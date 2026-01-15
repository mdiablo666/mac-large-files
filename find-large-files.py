#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# File extensions to exclude
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', 
              '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2', '.mxf', '.ogv'}
PHOTO_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
              '.webp', '.svg', '.ico', '.heic', '.heif', '.raw', '.psd', '.ai'}

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f}TB"

def find_large_files(search_path='.', size_mb=100):
    size_bytes = size_mb * 1024 * 1024
    excluded_exts = VIDEO_EXTS | PHOTO_EXTS
    
    print(f"🔍 Searching for files larger than {size_mb}MB in: {search_path}")
    print("⏭️  Excluding video and photo files...")
    print("─" * 50)
    
    large_files = []
    
    for root, dirs, files in os.walk(search_path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                file_size = os.path.getsize(filepath)
                if file_size > size_bytes:
                    ext = Path(file).suffix.lower()
                    if ext not in excluded_exts:
                        large_files.append((filepath, file_size))
            except (OSError, PermissionError):
                pass
    
    # Sort by size (largest first)
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    for filepath, size in large_files:
        print(f"{format_size(size):>10}  {filepath}")
    
    print("─" * 50)
    print(f"✅ Found {len(large_files)} file(s) matching criteria")

if __name__ == "__main__":
    search_path = sys.argv[1] if len(sys.argv) > 1 else '.''
    size_mb = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    find_large_files(search_path, size_mb)