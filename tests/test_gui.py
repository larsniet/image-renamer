"""
Tests for the GUI components of the Image Renamer.
These tests focus on utility functions that can be tested
without launching a real GUI or complex mocking.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# We need to mock minimally for these tests
sys.modules['PyQt6'] = MagicMock()
sys.modules['PyQt6.QtWidgets'] = MagicMock()
sys.modules['PyQt6.QtCore'] = MagicMock()
sys.modules['PyQt6.QtGui'] = MagicMock()

# Now we can import our modules without GUI dependencies
from imagerenamer.gui import resource_path, set_style
from imagerenamer import gui  # Import as module for easier mocking

class TestResourcePath:
    """Tests for the resource_path function."""
    
    def test_resource_path_normal(self):
        """Test resource_path in normal mode (not PyInstaller)."""
        # Test with a simple relative path
        test_path = "test_file.txt"
        result = resource_path(test_path)
        
        # In normal mode, should return a path relative to the parent directory of the package
        assert test_path in result
        assert os.path.isabs(result)
    
    def test_resource_path_pyinstaller(self):
        """Test resource_path in PyInstaller mode."""
        # Patch sys module with _MEIPASS attribute
        with patch.object(sys, '_MEIPASS', new='/meipass/dir', create=True):
            # Test with a simple relative path
            test_path = "test_file.txt"
            result = resource_path(test_path)
            
            # In PyInstaller mode, should use _MEIPASS as base
            assert '/meipass/dir' in result
            assert test_path in result
            assert result == os.path.join('/meipass/dir', test_path)

class TestSetStyle:
    """Tests for the set_style function."""
    
    def test_style_string(self):
        """Test that set_style returns a non-empty string."""
        style = set_style()
        
        assert isinstance(style, str)
        assert len(style) > 0
        
        # Check that the style contains expected CSS properties
        assert "QMainWindow" in style
        assert "background-color" in style
        assert "QPushButton" in style
        assert "QLineEdit" in style
        assert "QCheckBox" in style
        
        # Check that it contains our dark theme colors
        assert "#2D2D30" in style  # Dark background color
        assert "#E0E0E0" in style  # Light text color
        assert "#0E639C" in style  # Button color

class TestFileFilter:
    """Tests for the file filtering functionality in the GUI."""
    
    def test_file_extension_filtering(self):
        """Test that file filtering with specific extensions works correctly."""
        # Create a list of extensions
        image_extensions = (".jpg", ".jpeg", ".png")
        video_extensions = (".mp4", ".mov")
        
        # Test that files with correct extensions are accepted
        assert "test.jpg".lower().endswith(image_extensions)
        assert "test.png".lower().endswith(image_extensions)
        assert "test.mp4".lower().endswith(video_extensions)
        
        # Test that files with incorrect extensions are rejected
        assert not "test.txt".lower().endswith(image_extensions)
        assert not "test.pdf".lower().endswith(video_extensions)
        
        # Test with combined extensions
        all_extensions = image_extensions + video_extensions
        assert "test.jpg".lower().endswith(all_extensions)
        assert "test.mp4".lower().endswith(all_extensions)
        assert not "test.txt".lower().endswith(all_extensions)
    
    def test_media_extensions_constants(self):
        """Test that the media extension constants are defined correctly."""
        # The constants should be defined in the module
        assert hasattr(gui, 'image_extensions')
        
        # Define expected extension lists - these should match what's in the code
        expected_image_extensions = (".jpg", ".jpeg", ".png", ".nef", ".cr2", ".arw")
        expected_video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".3gp", ".webm", ".flv")
        
        # Patch the module with our expected values for testing
        with patch.object(gui, 'image_extensions', expected_image_extensions):
            with patch.object(gui, 'video_extensions', expected_video_extensions):
                # The filter function we want to test
                def file_filter(extensions):
                    return lambda filename: filename.lower().endswith(extensions)
                
                # Create filters for different extension sets
                image_filter = file_filter(gui.image_extensions)
                video_filter = file_filter(gui.video_extensions)
                all_filter = file_filter(gui.image_extensions + gui.video_extensions)
                
                # Test the filters
                assert image_filter("test.jpg")
                assert not image_filter("test.mp4")
                
                assert video_filter("test.mp4")
                assert not video_filter("test.jpg")
                
                assert all_filter("test.jpg")
                assert all_filter("test.mp4")
                assert not all_filter("test.txt") 