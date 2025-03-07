from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(os.path.join('imagerenamer', '__init__.py'), 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.0.0'

# Read the long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="modern-image-renamer",
    version=version,
    author="Lars van der Niet",
    description="Rename image files based on their creation date from EXIF metadata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larsniet/image-renamer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=9.0.0",
        "PyQt6>=6.4.0",
    ],
    entry_points={
        'console_scripts': [
            'imagerenamer=imagerenamer.cli:main',
            'imagerenamer-gui=imagerenamer.gui:main',
        ],
    },
    scripts=[
        'scripts/imagerenamer-cli',
        'scripts/imagerenamer-gui',
    ],
) 