#!/usr/bin/env python3
"""
Command-line interface for the Image Renamer tool.
"""

import sys
import argparse
import os
from imagerenamer.core import rename_images
from imagerenamer import __version__

def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Rename image and video files based on their creation date from metadata."
    )
    
    parser.add_argument(
        "folder",
        help="Path to the folder containing images and videos to rename"
    )
    
    parser.add_argument(
        "-f", "--format",
        default="%Y-%m-%d_%H-%M-%S",
        help="Format string for the new filenames (default: '%%Y-%%m-%%d_%%H-%%M-%%S')"
    )
    
    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        help="Create backups of the original files"
    )
    
    parser.add_argument(
        "-r", "--remove-duplicates",
        action="store_true",
        help="Remove duplicates instead of renaming them with suffixes"
    )
    
    parser.add_argument(
        "--include-videos",
        action="store_true",
        help="Include video files (mp4, mov, avi, etc.) in addition to images"
    )
    
    parser.add_argument(
        "-v", "--version", 
        action="version", 
        version=f"Image Renamer {__version__}"
    )
    
    args = parser.parse_args()
    
    # Check if folder exists
    if not os.path.isdir(args.folder):
        print(f"Error: Folder '{args.folder}' does not exist")
        return 1
    
    # Set up file extensions filter based on options
    image_extensions = (".jpg", ".jpeg", ".png", ".nef", ".cr2", ".arw")
    video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".3gp", ".webm", ".flv")
    
    if args.include_videos:
        media_extensions = image_extensions + video_extensions
    else:
        media_extensions = image_extensions
    
    # Create a filter function
    def file_filter(filename):
        return filename.lower().endswith(media_extensions)
    
    # Run the renaming process
    stats = rename_images(
        args.folder,
        args.backup,
        args.format,
        remove_duplicates=args.remove_duplicates,
        file_filter=file_filter
    )
    
    # Print summary
    if not stats["error"]:
        print("\n--- Summary ---")
        print(f"Total image files: {stats['total']}")
        print(f"Files renamed: {stats['renamed']}")
        print(f"Files skipped: {stats['skipped']}")
        
        if 'removed_duplicates' in stats and stats['removed_duplicates'] > 0:
            print(f"Duplicates removed: {stats['removed_duplicates']}")
            
        if stats["renamed"] > 0:
            print("\n✅ Renaming completed successfully!")
        else:
            print("\nNo files were renamed.")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main()) 