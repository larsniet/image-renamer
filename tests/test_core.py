"""
Tests for the core functionality of the Image Renamer.
"""

import os
import pytest
from datetime import datetime
from pathlib import Path
from imagerenamer.core import get_exif_creation_date, rename_images

def test_get_exif_creation_date(sample_image_directory):
    """Test extracting EXIF creation date from an image."""
    # Get the path to an image
    image_path = os.path.join(sample_image_directory, "IMG_001.jpg")
    
    # In our test environment, we don't actually have EXIF data
    # Our real test is that the function handles this properly and falls back
    # to file creation date
    creation_date = get_exif_creation_date(image_path)
    
    # This should be None since our test images don't have EXIF data
    assert creation_date is None
    
    # Test with a non-existent file
    non_existent_path = os.path.join(sample_image_directory, "non_existent.jpg")
    creation_date_non_existent = get_exif_creation_date(non_existent_path)
    assert creation_date_non_existent is None

def test_rename_images_basic(sample_image_directory):
    """Test renaming images with basic options."""
    # Count the original files
    original_files = os.listdir(sample_image_directory)
    image_files = [f for f in original_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Run the rename function
    stats = rename_images(sample_image_directory, create_backup=False)
    
    # Assertions
    assert not stats.get('error')
    assert stats['total'] == len(image_files)
    assert stats['renamed'] + stats['skipped'] == len(image_files)
    
    # Check that the files have been renamed
    renamed_files = os.listdir(sample_image_directory)
    renamed_image_files = [f for f in renamed_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # The number of image files should remain the same
    assert len(renamed_image_files) == len(image_files)
    
    # Check that the names have the correct format (YYYY-MM-DD_HH-MM-SS.jpg)
    for file in renamed_image_files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            # The file should match the date format pattern
            name_without_ext = os.path.splitext(file)[0]
            assert len(name_without_ext) >= 19  # Basic length check for YYYY-MM-DD_HH-MM-SS format
            
            # Format should have hyphens and underscores in the right places
            assert name_without_ext[4] == "-" and name_without_ext[7] == "-"
            assert name_without_ext[10] == "_"
            assert name_without_ext[13] == "-" and name_without_ext[16] == "-"

def test_rename_images_with_backup(sample_image_directory):
    """Test renaming images with backup option."""
    # Count the original files
    original_files = os.listdir(sample_image_directory)
    image_files = [f for f in original_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Run the rename function with backup
    stats = rename_images(sample_image_directory, create_backup=True)
    
    # Assertions
    assert not stats.get('error')
    
    # Check that a backup directory was created
    backup_dir = os.path.join(sample_image_directory, "backup")
    assert os.path.isdir(backup_dir)
    
    # Check that the backup directory contains the original files
    backup_files = os.listdir(backup_dir)
    backup_image_files = [f for f in backup_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    assert len(backup_image_files) == len(image_files)
    
    # All original image filenames should be in the backup
    for file in image_files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            assert file in backup_files

def test_rename_images_custom_format(sample_image_directory):
    """Test renaming images with a custom format."""
    # Custom format
    custom_format = "%Y%m%d_%H%M%S"
    
    # Run the rename function with the custom format
    stats = rename_images(sample_image_directory, create_backup=False, format_string=custom_format)
    
    # Assertions
    assert not stats.get('error')
    
    # Check that the files have been renamed with the custom format
    renamed_files = os.listdir(sample_image_directory)
    renamed_image_files = [f for f in renamed_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Check that the names have the correct format (YYYYMMDD_HHMMSS.jpg)
    for file in renamed_image_files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            # The file should match the date format pattern
            name_without_ext = os.path.splitext(file)[0]
            assert len(name_without_ext) >= 15  # Basic length check for YYYYMMDD_HHMMSS format
            
            # Format should have underscore in the right place
            assert name_without_ext[8] == "_"
            
            # Should be all digits except for the underscore
            assert name_without_ext.replace("_", "").isdigit()

def test_rename_images_invalid_directory():
    """Test renaming images with an invalid directory."""
    # Run the rename function with a non-existent directory
    stats = rename_images("/non/existent/directory")
    
    # Assertions
    assert stats.get('error')
    assert stats['total'] == 0
    assert stats['renamed'] == 0
    assert stats['skipped'] == 0

def test_rename_images_with_callback(sample_image_directory):
    """Test renaming images with a callback function."""
    # Setup a callback function to collect messages
    messages = []
    def callback(message):
        messages.append(message)
    
    # Run the rename function with the callback
    stats = rename_images(sample_image_directory, callback=callback)
    
    # Assertions
    assert not stats.get('error')
    assert len(messages) > 0
    
    # Check for expected message types in the callback
    assert any("Found" in message for message in messages)
    assert any("Renamed" in message for message in messages) or any("Skipping" in message for message in messages) 