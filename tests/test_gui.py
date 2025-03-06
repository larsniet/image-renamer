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

# Import only the specific functions we want to test
from imagerenamer.gui import resource_path, set_style

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