"""
Core functionality for renaming images based on EXIF metadata.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_creation_date(image_path):
    """
    Extract the creation date from image EXIF metadata.
    Returns a datetime object or None if no date found.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        datetime: Creation date as datetime object or None
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return None

def rename_images(folder_path, create_backup=False, format_string="%Y-%m-%d_%H-%M-%S", callback=None, 
                 remove_duplicates=False, file_filter=None):
    """
    Rename all image and video files in the folder based on their creation date.
    
    Args:
        folder_path (str): Path to the folder containing images and videos
        create_backup (bool): Whether to create a backup of the original files
        format_string (str): Format string for the new filename (strftime format)
        callback (function): Optional callback function for progress updates
        remove_duplicates (bool): Whether to remove duplicate files instead of renaming with suffixes
        file_filter (function): Optional function to filter which files to process
        
    Returns:
        dict: Statistics about the operation
    """
    # Validate folder exists
    if not os.path.isdir(folder_path):
        message = f"Error: Folder '{folder_path}' does not exist"
        if callback:
            callback(message)
        else:
            print(message)
        return {"total": 0, "renamed": 0, "skipped": 0, "removed_duplicates": 0, "error": True}
    
    # Create backup folder if needed
    backup_folder = None
    if create_backup:
        backup_folder = os.path.join(folder_path, "backup")
        os.makedirs(backup_folder, exist_ok=True)
        message = f"Created backup folder: {backup_folder}"
        if callback:
            callback(message)
        else:
            print(message)
    
    # Track statistics
    total_files = 0
    renamed_files = 0
    skipped_files = 0
    removed_duplicates = 0
    
    # Get image and video files
    if file_filter is None:
        # Default extensions if no filter is provided
        image_extensions = (".jpg", ".jpeg", ".png", ".nef", ".cr2", ".arw")
        video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".3gp", ".webm", ".flv")
        media_extensions = image_extensions + video_extensions
        
        # Create a default filter function
        def file_filter(filename):
            return filename.lower().endswith(media_extensions)
    
    media_files = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        # Skip directories and files that don't match the filter
        if os.path.isdir(file_path) or not file_filter(file):
            continue
        media_files.append(file)
    
    total_files = len(media_files)
    message = f"Found {total_files} media files to process"
    if callback:
        callback(message)
    else:
        print(message)
    
    # Process all files in the folder
    for file in media_files:
        file_path = os.path.join(folder_path, file)
        
        # Try to get creation date from EXIF metadata
        creation_date = get_exif_creation_date(file_path)
        
        # If no EXIF data, fallback to file creation timestamp
        if not creation_date:
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time)
            message = f"No EXIF data for {file}, using file creation time"
            if callback:
                callback(message)
            else:
                print(message)
        
        # Generate new filename
        file_extension = Path(file).suffix.lower()
        new_filename = creation_date.strftime(format_string) + file_extension
        new_path = os.path.join(folder_path, new_filename)
        
        # Avoid overwriting existing files
        counter = 1
        while os.path.exists(new_path) and new_path != file_path:
            # If removing duplicates is enabled, skip this file
            if remove_duplicates:
                message = f"Skipping duplicate {file} (same creation date as existing {new_filename})"
                if callback:
                    callback(message)
                else:
                    print(message)
                skipped_files += 1
                removed_duplicates += 1
                break
            
            # Otherwise, add a suffix to the filename
            new_filename = creation_date.strftime(format_string) + f"_{counter}" + file_extension
            new_path = os.path.join(folder_path, new_filename)
            counter += 1
        
        # If the new filename is the same as the old one, skip
        if new_path == file_path:
            message = f"Skipping {file} (already has correct name)"
            if callback:
                callback(message)
            else:
                print(message)
            skipped_files += 1
            continue
            
        # Create backup if requested
        if create_backup:
            shutil.copy2(file_path, os.path.join(backup_folder, file))
        
        # Rename the file
        try:
            os.rename(file_path, new_path)
            message = f"Renamed: {file} → {new_filename}"
            if callback:
                callback(message)
            else:
                print(message)
            renamed_files += 1
        except Exception as e:
            message = f"Error renaming {file}: {e}"
            if callback:
                callback(message)
            else:
                print(message)
            skipped_files += 1
    
    # Return statistics
    stats = {
        "total": total_files,
        "renamed": renamed_files,
        "skipped": skipped_files,
        "removed_duplicates": removed_duplicates,
        "error": False
    }
    
    return stats 