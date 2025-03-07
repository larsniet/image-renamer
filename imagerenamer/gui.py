#!/usr/bin/env python3
"""
Graphical user interface for the Image Renamer tool.
"""

import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QFileDialog, QCheckBox, 
    QComboBox, QProgressBar, QTextEdit, QGroupBox, QFormLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QIcon, QFont, QPixmap, QColor, QPalette

from imagerenamer.core import rename_images
from imagerenamer import __version__

# Define file extension constants
image_extensions = (".jpg", ".jpeg", ".png", ".nef", ".cr2", ".arw")
video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".3gp", ".webm", ".flv")

# Find the application resource path
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    return os.path.join(base_path, relative_path)

class RenamerWorker(QThread):
    """Worker thread to handle the renaming process."""
    progress_update = pyqtSignal(str)
    completed = pyqtSignal(dict)
    
    def __init__(self, folder_path, create_backup, format_string, remove_duplicates=False):
        super().__init__()
        self.folder_path = folder_path
        self.create_backup = create_backup
        self.format_string = format_string
        self.remove_duplicates = remove_duplicates
        
        # Default to both image and video extensions
        self.media_extensions = image_extensions + video_extensions
        
    def run(self):
        """Run the renaming process in a separate thread."""
        
        # Define callback function for progress updates
        def update_callback(message):
            self.progress_update.emit(message)
        
        # Custom filter function to pass to the core rename_images function
        def file_filter(filename):
            return filename.lower().endswith(self.media_extensions)
        
        # Run the renaming process
        stats = rename_images(
            self.folder_path,
            self.create_backup,
            self.format_string,
            update_callback,
            self.remove_duplicates,
            file_filter
        )
        
        # Emit completion signal with statistics
        self.completed.emit(stats)

def set_style():
    """Set application style with a dark theme."""
    style = """
    QMainWindow, QDialog {
        background-color: #2D2D30;
        color: #E0E0E0;
    }
    QWidget {
        color: #E0E0E0;
    }
    QGroupBox {
        font-weight: bold;
        border: 1px solid #3F3F46;
        border-radius: 6px;
        margin-top: 12px;
        padding-top: 10px;
        background-color: #252526;
        color: #E0E0E0;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
        color: #E0E0E0;
    }
    QPushButton {
        border: 1px solid #3F3F46;
        border-radius: 4px;
        background-color: #333337;
        color: #E0E0E0;
        min-width: 80px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #3E3E42;
        border-color: #007ACC;
    }
    QPushButton:pressed {
        background-color: #2D2D30;
    }
    #start_btn {
        background-color: #0E639C;
        color: white;
        font-weight: bold;
        border-color: #007ACC;
    }
    #start_btn:hover {
        background-color: #1177BB;
    }
    QLineEdit, QComboBox {
        border: 1px solid #3F3F46;
        border-radius: 4px;
        padding: 4px;
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    QComboBox::drop-down {
        border: 0px;
    }
    QComboBox::down-arrow {
        width: 14px;
        height: 14px;
    }
    QComboBox QAbstractItemView {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #3F3F46;
    }
    QTextEdit {
        border: 1px solid #3F3F46;
        border-radius: 4px;
        background-color: #1E1E1E;
        color: #E0E0E0;
        font-family: monospace;
    }
    QLabel {
        color: #E0E0E0;
    }
    QCheckBox {
        color: #E0E0E0;
    }
    QCheckBox::indicator {
        width: 13px;
        height: 13px;
    }
    QStatusBar {
        background-color: #007ACC;
        color: white;
    }
    QProgressBar {
        border: 1px solid #3F3F46;
        border-radius: 4px;
        background-color: #1E1E1E;
        text-align: center;
        color: #E0E0E0;
    }
    QProgressBar::chunk {
        background-color: #0E639C;
        width: 10px;
    }
    """
    return style

class ImageRenamerApp(QMainWindow):
    """Main window for the Image Renamer application."""
    
    def __init__(self):
        super().__init__()
        
        # Load settings
        self.settings = QSettings("ImageRenamer", "ImageRenamerApp")
        
        # Set window properties
        self.setWindowTitle(f"Image Renamer v{__version__}")
        self.setMinimumSize(700, 600)
        
        # Set application icon
        icon_path = resource_path("resources/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Fall back to looking for other icon files
            fallback_icons = [
                "resources/icon.ico"
            ]
            
            for fallback in fallback_icons:
                fallback_path = resource_path(fallback)
                if os.path.exists(fallback_path):
                    self.setWindowIcon(QIcon(fallback_path))
                    break
        
        # Initialize UI
        self.init_ui()
        
        # Load previous settings
        self.load_settings()
        
        # Set the app style
        self.setStyleSheet(set_style())
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Add title and description
        title_label = QLabel("Image Renamer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        description_label = QLabel(
            "Rename your images and videos based on their creation date from metadata."
        )
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_font = QFont()
        description_font.setPointSize(10)
        description_label.setFont(description_font)
        
        # Directory selection
        dir_group = QGroupBox("Media Directory")
        dir_layout = QHBoxLayout()
        dir_layout.setContentsMargins(15, 20, 15, 15)
        
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Select folder containing images and videos...")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(self.dir_input, 3)
        dir_layout.addWidget(browse_btn, 1)
        dir_group.setLayout(dir_layout)
        
        # Options group
        options_group = QGroupBox("Rename Options")
        options_layout = QFormLayout()
        options_layout.setContentsMargins(15, 20, 15, 15)
        options_layout.setSpacing(10)
        
        # Format selection
        self.format_dropdown = QComboBox()
        format_options = [
            ("%Y-%m-%d_%H-%M-%S", "2023-04-25_14-30-15.jpg (Default)"),
            ("%Y%m%d_%H%M%S", "20230425_143015.jpg"),
            ("%Y-%m-%d_%Hh%Mm%Ss", "2023-04-25_14h30m15s.jpg"),
            ("%Y%m%d-%H%M%S", "20230425-143015.jpg"),
        ]
        
        for format_string, description in format_options:
            self.format_dropdown.addItem(description, format_string)
        
        # Custom format
        self.custom_format = QLineEdit()
        self.custom_format.setPlaceholderText("Custom format (e.g. %Y_%m_%d)")
        
        # Backup checkbox
        self.backup_checkbox = QCheckBox("Create backups of original files")
        self.backup_checkbox.setChecked(True)
        
        # Duplicate handling checkbox
        self.remove_duplicates_checkbox = QCheckBox("Remove duplicates instead of renaming with suffixes")
        self.remove_duplicates_checkbox.setChecked(False)
        
        # Media type selection checkbox
        self.include_videos_checkbox = QCheckBox("Include video files (mp4, mov, avi, etc.)")
        self.include_videos_checkbox.setChecked(True)
        
        options_layout.addRow("Format:", self.format_dropdown)
        options_layout.addRow("Custom format:", self.custom_format)
        options_layout.addRow(self.backup_checkbox)
        options_layout.addRow(self.remove_duplicates_checkbox)
        options_layout.addRow(self.include_videos_checkbox)
        options_group.setLayout(options_layout)
        
        # Progress and log
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(15, 20, 15, 15)
        progress_layout.setSpacing(10)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(200)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.log_output)
        progress_group.setLayout(progress_layout)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.start_btn = QPushButton("Start Renaming")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.start_renaming)
        self.start_btn.setMinimumHeight(40)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_renaming)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setMinimumHeight(40)
        
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        # Add all components to main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(description_label)
        main_layout.addSpacing(10)
        main_layout.addWidget(dir_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(progress_group)
        main_layout.addLayout(buttons_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def browse_directory(self):
        """Open a file dialog to select a directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            self.dir_input.setText(directory)
            # Count media files
            media_count = self.count_media_files(directory)
            self.statusBar().showMessage(f"Found {media_count} media files in selected directory")
    
    def count_media_files(self, directory):
        """Count the number of image and video files in a directory."""
        # Only include video extensions if the checkbox is checked
        if hasattr(self, 'include_videos_checkbox') and self.include_videos_checkbox.isChecked():
            media_extensions = image_extensions + video_extensions
        else:
            media_extensions = image_extensions
            
        count = 0
        
        for file in os.listdir(directory):
            if file.lower().endswith(media_extensions) and os.path.isfile(os.path.join(directory, file)):
                count += 1
                
        return count
    
    def start_renaming(self):
        """Start the renaming process."""
        directory = self.dir_input.text().strip()
        
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "Invalid Directory", 
                              "Please select a valid directory containing images.")
            return
        
        # Get format string
        if self.custom_format.text().strip():
            format_string = self.custom_format.text().strip()
        else:
            format_string = self.format_dropdown.currentData()
        
        create_backup = self.backup_checkbox.isChecked()
        remove_duplicates = self.remove_duplicates_checkbox.isChecked()
        include_videos = self.include_videos_checkbox.isChecked()
        
        # Clear log and show progress bar
        self.log_output.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Disable inputs during process
        self.toggle_inputs(False)
        
        # Create and start worker thread
        self.worker = RenamerWorker(directory, create_backup, format_string, remove_duplicates)
        
        # Set the file extensions to use
        if include_videos:
            self.worker.media_extensions = image_extensions + video_extensions
        else:
            self.worker.media_extensions = image_extensions
            
        self.worker.progress_update.connect(self.update_log)
        self.worker.completed.connect(self.process_completed)
        self.worker.start()
        
        # Save settings
        self.save_settings()
    
    def cancel_renaming(self):
        """Cancel the renaming process."""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self.update_log("Process cancelled by user")
            self.toggle_inputs(True)
            self.progress_bar.setVisible(False)
    
    def update_log(self, message):
        """Update the log output with a new message."""
        self.log_output.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def process_completed(self, stats):
        """Handle completion of the renaming process."""
        # Hide progress bar and enable inputs
        self.progress_bar.setVisible(False)
        self.toggle_inputs(True)
        
        # Show summary
        self.update_log("\n--- Summary ---")
        self.update_log(f"Total image files: {stats['total']}")
        self.update_log(f"Files renamed: {stats['renamed']}")
        self.update_log(f"Files skipped: {stats['skipped']}")
        
        if 'removed_duplicates' in stats and stats['removed_duplicates'] > 0:
            self.update_log(f"Duplicates removed: {stats['removed_duplicates']}")
        
        if stats['renamed'] > 0:
            self.update_log("\n✅ Renaming completed successfully!")
        else:
            self.update_log("\nNo files were renamed.")
        
        # Show in status bar
        self.statusBar().showMessage(f"Completed: {stats['renamed']} files renamed, {stats['skipped']} skipped")
        
        # Show completion dialog
        summary_text = f"Renaming completed!\n\n{stats['renamed']} files renamed\n{stats['skipped']} files skipped"
        if 'removed_duplicates' in stats and stats['removed_duplicates'] > 0:
            summary_text += f"\n{stats['removed_duplicates']} duplicates removed"
            
        QMessageBox.information(self, "Process Complete", summary_text)
    
    def toggle_inputs(self, enabled):
        """Enable or disable input controls."""
        self.dir_input.setEnabled(enabled)
        self.format_dropdown.setEnabled(enabled)
        self.custom_format.setEnabled(enabled)
        self.backup_checkbox.setEnabled(enabled)
        self.remove_duplicates_checkbox.setEnabled(enabled)
        self.include_videos_checkbox.setEnabled(enabled)
        self.start_btn.setEnabled(enabled)
        self.cancel_btn.setEnabled(not enabled)
    
    def save_settings(self):
        """Save application settings."""
        self.settings.setValue("directory", self.dir_input.text())
        self.settings.setValue("format_index", self.format_dropdown.currentIndex())
        self.settings.setValue("custom_format", self.custom_format.text())
        self.settings.setValue("create_backup", self.backup_checkbox.isChecked())
        self.settings.setValue("remove_duplicates", self.remove_duplicates_checkbox.isChecked())
        self.settings.setValue("include_videos", self.include_videos_checkbox.isChecked())
    
    def load_settings(self):
        """Load application settings."""
        directory = self.settings.value("directory", "")
        format_index = int(self.settings.value("format_index", 0))
        custom_format = self.settings.value("custom_format", "")
        create_backup = self.settings.value("create_backup", True, type=bool)
        remove_duplicates = self.settings.value("remove_duplicates", False, type=bool)
        include_videos = self.settings.value("include_videos", True, type=bool)
        
        self.dir_input.setText(directory)
        self.format_dropdown.setCurrentIndex(format_index)
        self.custom_format.setText(custom_format)
        self.backup_checkbox.setChecked(create_backup)
        self.remove_duplicates_checkbox.setChecked(remove_duplicates)
        self.include_videos_checkbox.setChecked(include_videos)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Save settings when closing
        self.save_settings()
        event.accept()

def main():
    """Main entry point for the GUI application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = ImageRenamerApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 