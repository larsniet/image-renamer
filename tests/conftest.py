"""
Pytest configuration and fixtures for the Image Renamer test suite.
"""

import os
import pytest
import shutil
import tempfile
import time
from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    # Create a temporary directory
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Clean up after the test
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_image_directory(temp_dir):
    """Create a directory with sample images for testing."""
    # Create sample image files with different creation dates
    for i in range(1, 4):
        image_path = os.path.join(temp_dir, f"IMG_00{i}.jpg")
        create_sample_image(image_path)
        
        # Set different modification times to simulate different creation dates
        # for images without EXIF data
        mod_time = time.time() - (i * 3600)  # Each file 1 hour apart
        os.utime(image_path, (mod_time, mod_time))

    # Create a non-image file
    with open(os.path.join(temp_dir, "not_an_image.txt"), "w") as f:
        f.write("This is not an image file")
        
    return temp_dir

def create_sample_image(path, size=(100, 100), color=(255, 0, 0)):
    """Create a sample image file."""
    # Create a sample image
    image = Image.new("RGB", size, color)
    
    # Save the image
    image.save(path)
    
    return path 