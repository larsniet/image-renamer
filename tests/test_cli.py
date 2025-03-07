"""
Tests for the command-line interface of the Image Renamer.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from imagerenamer.cli import main
import shutil

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
    image_extensions = (".jpg", ".jpeg", ".png", ".nef", ".cr2", ".arw")
    video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".3gp", ".webm", ".flv")
    media_extensions = image_extensions + video_extensions
    
    original_files = os.listdir(sample_image_directory)
    media_files = [f for f in original_files if f.lower().endswith(media_extensions)]
    
    # Mock sys.argv and run the main function
    with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory]):
        exit_code = main()
    
    # Check exit code
    assert exit_code == 0
    
    # Check that files were renamed
    renamed_files = os.listdir(sample_image_directory)
    renamed_media_files = [f for f in renamed_files if f.lower().endswith(media_extensions)]
    
    # The number of media files should remain the same
    assert len(renamed_media_files) == len(media_files)

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

def test_cli_main_with_remove_duplicates(sample_image_directory):
    """Test the CLI with the remove_duplicates option."""
    # First, create a situation with duplicates
    # Let's copy an existing image to ensure we have at least one duplicate
    image_files = [f for f in os.listdir(sample_image_directory) 
                  if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    if len(image_files) > 0:
        # Copy the first image with a different name
        source_path = os.path.join(sample_image_directory, image_files[0])
        duplicate_name = "DUPLICATE_" + image_files[0]
        duplicate_path = os.path.join(sample_image_directory, duplicate_name)
        shutil.copy2(source_path, duplicate_path)
        
        # For testing purposes, ensure the file has the same creation time
        # by setting the access and modified times to the same as the source file
        src_stat = os.stat(source_path)
        os.utime(duplicate_path, (src_stat.st_atime, src_stat.st_mtime))
        
        # Get the number of image files after adding the duplicate
        current_files = os.listdir(sample_image_directory)
        current_image_count = len([f for f in current_files 
                                 if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        
        # Mock sys.argv and run the main function with --remove-duplicates
        with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory, '--remove-duplicates']):
            result = main()
        
        # Check exit code
        assert result == 0
        
        # Verify that duplicates were removed
        after_files = os.listdir(sample_image_directory)
        after_image_count = len([f for f in after_files 
                                if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        
        # The number of image files should be less than before (duplicates removed)
        assert after_image_count < current_image_count

def test_cli_help_includes_remove_duplicates_option(capsys):
    """Test that the --remove-duplicates option is included in the help text."""
    # Test the help option
    with pytest.raises(SystemExit) as excinfo:
        with patch.object(sys, 'argv', ['imagerenamer', '--help']):
            main()
    
    # Should exit with code 0 (success)
    assert excinfo.value.code == 0
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check that the help text includes the new option
    assert "--remove-duplicates" in captured.out 

def test_cli_main_with_include_videos(sample_image_directory):
    """Test the CLI with the include-videos option."""
    # Create test files - one image and one video
    test_image_path = os.path.join(sample_image_directory, "test_image.jpg")
    test_video_path = os.path.join(sample_image_directory, "test_video.mp4")
    
    with open(test_image_path, "w") as f:
        f.write("test image file")
    
    with open(test_video_path, "w") as f:
        f.write("test video file")
    
    # First, test without --include-videos flag (should process only images)
    with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory]):
        with patch('imagerenamer.cli.rename_images') as mock_rename:
            mock_rename.return_value = {"total": 1, "renamed": 1, "skipped": 0, "error": False}
            main()
            
            # Get the file_filter function that was passed
            args, kwargs = mock_rename.call_args
            file_filter = kwargs.get('file_filter')
            
            # Test that the filter accepts image files but rejects video files
            assert file_filter("test.jpg")
            assert not file_filter("test.mp4")
    
    # Now test with --include-videos flag (should process both)
    with patch.object(sys, 'argv', ['imagerenamer', sample_image_directory, '--include-videos']):
        with patch('imagerenamer.cli.rename_images') as mock_rename:
            mock_rename.return_value = {"total": 2, "renamed": 2, "skipped": 0, "error": False}
            main()
            
            # Get the file_filter function that was passed
            args, kwargs = mock_rename.call_args
            file_filter = kwargs.get('file_filter')
            
            # Test that the filter accepts both image and video files
            assert file_filter("test.jpg")
            assert file_filter("test.mp4")
    
    # Cleanup
    try:
        os.remove(test_image_path)
        os.remove(test_video_path)
    except:
        pass  # Ignore cleanup errors

def test_cli_help_includes_video_option(capsys):
    """Test that the --include-videos option is included in the help text."""
    # Test the help option
    with pytest.raises(SystemExit) as excinfo:
        with patch.object(sys, 'argv', ['imagerenamer', '--help']):
            main()
    
    # Should exit with code 0 (success)
    assert excinfo.value.code == 0
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check that the help text includes the new option
    assert "--include-videos" in captured.out 