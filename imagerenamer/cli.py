#!/usr/bin/env python3
"""
Command-line interface for the Image Renamer tool.
"""

import sys
import argparse
from imagerenamer.core import rename_images
from imagerenamer import __version__

def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Rename image files based on their creation date from EXIF metadata."
    )
    
    parser.add_argument("folder", help="Path to the folder containing images")
    parser.add_argument(
        "-b", "--backup", 
        action="store_true", 
        help="Create backup of original files"
    )
    parser.add_argument(
        "-f", "--format", 
        default="%Y-%m-%d_%H-%M-%S",
        help="Format string for the new filename (default: '%%Y-%%m-%%d_%%H-%%M-%%S')"
    )
    parser.add_argument(
        "-v", "--version", 
        action="version", 
        version=f"Image Renamer {__version__}"
    )
    
    args = parser.parse_args()
    
    # Run the renaming process
    stats = rename_images(args.folder, args.backup, args.format)
    
    # Print summary
    print("\n--- Summary ---")
    print(f"Total image files: {stats['total']}")
    print(f"Files renamed: {stats['renamed']}")
    print(f"Files skipped: {stats['skipped']}")
    
    if stats['renamed'] > 0:
        print("\n✅ Renaming completed successfully!")
    else:
        print("\nNo files were renamed.")
    
    return 0 if not stats.get('error') else 1

if __name__ == "__main__":
    sys.exit(main()) 