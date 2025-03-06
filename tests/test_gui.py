"""
Tests for the GUI components of the Image Renamer.
These tests focus on utility functions and components that can be tested
without launching a real GUI or needing complex mocking.
"""

import sys
import pytest
from unittest.mock import patch, MagicMock

# We need to mock the QApplication before importing PyQt modules
sys.modules['PyQt6'] = MagicMock()
sys.modules['PyQt6.QtWidgets'] = MagicMock()
sys.modules['PyQt6.QtCore'] = MagicMock()
sys.modules['PyQt6.QtGui'] = MagicMock()

# Now we can safely import from imagerenamer.gui
from imagerenamer.gui import set_style

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