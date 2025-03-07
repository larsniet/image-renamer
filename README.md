# Image Renamer

[![Tests](https://github.com/larsniet/image-renamer/actions/workflows/tests.yml/badge.svg)](https://github.com/larsniet/image-renamer/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/larsniet/image-renamer/branch/main/graph/badge.svg)](https://codecov.io/gh/larsniet/image-renamer)
[![PyPI version](https://badge.fury.io/py/modern-image-renamer.svg)](https://badge.fury.io/py/modern-image-renamer)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/larsniet/image-renamer)](https://github.com/larsniet/image-renamer/releases)

A Python application that renames image and video files based on their creation date from metadata.

## Problem Solved

Digital cameras often reset their file numbering when SD cards are formatted, making it difficult to organize photos chronologically. This application automatically renames all images and videos in a folder using their creation date and time from the metadata.

## Features

- Renames image files using the creation date from EXIF metadata
- Optional support for video files (mp4, mov, avi, etc.)
- Falls back to file creation time if no EXIF data is available
- Supports JPG, JPEG, PNG, NEF, CR2, and ARW file formats
- Optional backup of original files
- Customizable filename format
- Prevents duplicate filenames by adding a counter
- Option to remove duplicate files instead of renaming them
- Beautiful and user-friendly GUI interface
- Remembers your previous settings

## Screenshots

![Image Renamer GUI](./screenshots/gui.png)

## Requirements

- Python 3.6 or higher
- Pillow library (for reading EXIF data)
- PyQt6 (for the GUI version)

## Installation

### Quick Install (Prebuilt Binaries)

The easiest way to get started is to download the pre-built executable for your operating system:

1. Go to the [Releases page](https://github.com/larsniet/image-renamer/releases/latest)
2. Download the appropriate file for your system:
   - **Windows**: Download `imagerenamer-windows.exe`
   - **macOS**: Download `imagerenamer-macos.zip`, extract and open the app
     - **Important**: When first opening the app, you may see a security warning. Instead of clicking the app directly, right-click (or Ctrl+click) on it and select "Open" from the menu. When prompted, click "Open" again. You only need to do this once.
   - **Linux**: Download `imagerenamer-linux`, make it executable with `chmod +x imagerenamer-linux`, and run it

No installation is required - just download and run!

### From Source

1. Clone this repository:
   ```bash
   git clone https://github.com/larsniet/image-renamer.git
   cd image-renamer
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

### From PyPI

```bash
pip install modern-image-renamer
```

## Usage

### GUI Application

There are several ways to launch the GUI:

```bash
# If installed via pip
imagerenamer-gui

# Or
python -m imagerenamer.gui

# Or from the source directory
./scripts/imagerenamer-gui
```

The GUI application provides an intuitive interface to:
- Select your image folder
- Choose from preset date formats or create a custom one
- Create backups of original files (optional)
- View real-time progress with a detailed log

### Command Line Interface

For command-line usage:

```bash
# If installed via pip
imagerenamer /path/to/images

# Or
python -m imagerenamer.cli /path/to/images

# Or from the source directory
./scripts/imagerenamer-cli /path/to/images
```

With backup option:

```bash
imagerenamer /path/to/images --backup
```

With custom filename format:

```bash
imagerenamer /path/to/images --format "%Y%m%d_%H%M%S"
```

Including video files:

```bash
imagerenamer /path/to/images --include-videos
```

Removing duplicates instead of renaming them:

```bash
imagerenamer /path/to/images --remove-duplicates
```

### Command Line Arguments

- `folder`: Path to the folder containing images (required)
- `-b, --backup`: Create backup of original files
- `-f, --format`: Format string for the new filename (default: '%Y-%m-%d_%H-%M-%S')
- `-r, --remove-duplicates`: Remove duplicates instead of renaming them with suffixes
- `--include-videos`: Include video files (mp4, mov, avi, etc.) in addition to images
- `-v, --version`: Show version information and exit

## Format String Options

The format string follows Python's `strftime()` format codes:

- `%Y`: 4-digit year (e.g., 2023)
- `%m`: 2-digit month (01-12)
- `%d`: 2-digit day (01-31)
- `%H`: 2-digit hour (00-23)
- `%M`: 2-digit minute (00-59)
- `%S`: 2-digit second (00-59)

Example formats:

- `%Y-%m-%d_%H-%M-%S` → 2023-04-25_14-30-15.jpg (default)
- `%Y%m%d_%H%M%S` → 20230425_143015.jpg
- `%Y-%m-%d_%Hh%Mm%Ss` → 2023-04-25_14h30m15s.jpg

## Project Structure

```
image-renamer/          # Project root
├── LICENSE             # MIT license file
├── README.md           # Project documentation
├── requirements.txt    # Dependencies
├── setup.py            # Package installation
├── pyproject.toml      # Modern Python packaging
├── .coveragerc         # Coverage configuration
├── pytest.ini          # pytest configuration
├── release.sh          # Release automation script
├── resources/          # Application resources
│   └── icon.png        # Application icon
├── imagerenamer/       # Main package
│   ├── __init__.py     # Package init, version info
│   ├── core.py         # Core functionality
│   ├── cli.py          # Command-line interface
│   └── gui.py          # GUI interface
├── scripts/            # Entry points
│   ├── imagerenamer-cli
│   └── imagerenamer-gui
├── tests/              # Test suite
│   ├── conftest.py     # pytest configuration
│   ├── test_core.py    # Core functionality tests
│   ├── test_cli.py     # CLI tests
│   └── test_gui.py     # GUI tests
└── .github/workflows/  # CI/CD workflows
    ├── build.yml       # Build workflow for releases
    ├── publish.yml     # PyPI publishing workflow
    └── tests.yml       # Testing workflow
```

## Running Tests

The project includes a comprehensive test suite using pytest. To run the tests:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run the tests
pytest

# Run tests with coverage report
pytest --cov=imagerenamer
```

The test suite includes:
- Unit tests for core functionality
- Command-line interface tests
- GUI component tests (without launching the actual GUI)

## Releases

### Automated Builds

This project uses GitHub Actions to automatically build and release packages for Windows, macOS, and Linux. When a new release tag is pushed (e.g., `v1.0.0`), the following happens:

1. Tests are run on all supported platforms
2. A new GitHub Release is created
3. Binary packages are built for each platform:
   - Windows: Standalone `.exe` file (zipped)
   - macOS: Standalone `.app` bundle (zipped)
   - Linux: Standalone executable (tarball)
4. Python package is published to PyPI

### Creating a New Release

This project includes an automated release script to simplify the process:

#### Using the Release Scripts

**Only for macOS/Linux users:**
```bash
./release.sh 1.0.1
```

These scripts will:
1. Ensure you're on the main branch
2. Run tests to verify everything works
3. Update the version number in the code
4. Commit and push the version change
5. Create and push a Git tag
6. GitHub Actions will automatically build and publish the release

#### Manual Release Process

If you prefer to release manually:

1. Update the version in `imagerenamer/__init__.py`
2. Commit the change: `git commit -m "Bump version to X.Y.Z"`
3. Push to main: `git push origin main`
4. Create a tag: `git tag vX.Y.Z`
5. Push the tag: `git push origin vX.Y.Z`

### Manual Installation from Releases

You can download the latest binary release for your platform from the [Releases page](https://github.com/larsniet/image-renamer/releases).

- **Windows**: Download and run `imagerenamer-windows.exe`
- **macOS**: 
  1. Download and extract `imagerenamer-macos.zip`
  2. Move `Image Renamer.app` to your Applications folder
  3. **Bypassing Security Warning**: When first launching, right-click (or Ctrl+click) on the app and select "Open" from the menu, then click "Open" in the dialog. This is only needed the first time you run the app.
  4. Alternatively, you can go to System Preferences → Security & Privacy → General and click "Open Anyway"
- **Linux**: Download `imagerenamer-linux`, make it executable with `chmod +x imagerenamer-linux`, and run it

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.