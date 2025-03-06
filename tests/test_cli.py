"""
Tests for the command-line interface of the Image Renamer.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from imagerenamer.cli import main

def test_cli_main_help(capsys):
    """Test the CLI help output."""
    # Test the help option
    with pytest.raises(SystemExit) as excinfo:
        with patch.object(sys, 'argv', ['imagerenamer', '--help']):
            main()
    
    # Should exit with code 0 (success)
    assert excinfo.value.code == 0
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check that the help text contains expected elements
    assert "usage:" in captured.out
    assert "folder" in captured.out
    assert "--backup" in captured.out
    assert "--format" in captured.out

def test_cli_main_version(capsys):
    """Test the CLI version output."""
    # Test the version option
    with pytest.raises(SystemExit) as excinfo:
        with patch.object(sys, 'argv', ['imagerenamer', '--version']):
            main()
    
    # Should exit with code 0 (success)
    assert excinfo.value.code == 0
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check that the version text contains "Image Renamer"
    assert "Image Renamer" in captured.out

def test_cli_main_rename(sample_image_directory):
    """Test the CLI rename functionality."""
    # Count original files
    original_files = os.listdir(sample_image_directory)
    image_files = [f for f in original_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Mock the command-line arguments
    with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory]):
        # Run the main function (should not raise an exception)
        exit_code = main()
    
    # Should return 0 (success)
    assert exit_code == 0
    
    # Check that the files have been renamed
    renamed_files = os.listdir(sample_image_directory)
    renamed_image_files = [f for f in renamed_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # The number of image files should remain the same
    assert len(renamed_image_files) == len(image_files)

def test_cli_main_rename_with_backup(sample_image_directory):
    """Test the CLI rename with backup option."""
    # Count original files
    original_files = os.listdir(sample_image_directory)
    image_files = [f for f in original_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Mock the command-line arguments with --backup
    with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory, '--backup']):
        # Run the main function
        exit_code = main()
    
    # Should return 0 (success)
    assert exit_code == 0
    
    # Check that a backup directory was created
    backup_dir = os.path.join(sample_image_directory, "backup")
    assert os.path.isdir(backup_dir)
    
    # Check that the backup directory contains the original files
    backup_files = os.listdir(backup_dir)
    backup_image_files = [f for f in backup_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    assert len(backup_image_files) == len(image_files)

def test_cli_main_rename_with_format(sample_image_directory):
    """Test the CLI rename with custom format option."""
    # Custom format
    custom_format = "%Y%m%d_%H%M%S"
    
    # Mock the command-line arguments with --format
    with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory, '--format', custom_format]):
        # Run the main function
        exit_code = main()
    
    # Should return 0 (success)
    assert exit_code == 0
    
    # Check that the files have been renamed with the custom format
    renamed_files = os.listdir(sample_image_directory)
    renamed_image_files = [f for f in renamed_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Check that the names have the correct format (YYYYMMDD_HHMMSS.jpg)
    for file in renamed_image_files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            # The file should match the date format pattern
            name_without_ext = os.path.splitext(file)[0]
            
            # Format should have underscore in the right place
            assert name_without_ext[8] == "_"
            
            # Should be all digits except for the underscore
            assert name_without_ext.replace("_", "").isdigit()

def test_cli_main_invalid_directory():
    """Test the CLI with an invalid directory."""
    # Mock the command-line arguments with an invalid directory
    with patch.object(sys, 'argv', ['imagerenamer', '/non/existent/directory']):
        # Run the main function
        exit_code = main()
    
    # Should return 1 (error)
    assert exit_code == 1 