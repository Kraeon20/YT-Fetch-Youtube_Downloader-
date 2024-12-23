from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QDialog
from PyQt5.QtCore import Qt
import sys
from downloader import download_video


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; font-family: Arial, sans-serif;")
        self.download_location = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        header_label = QLabel("Settings")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")

        download_location_label = QLabel("Download Location:")
        download_location_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        # Horizontal layout for QLineEdit and Browse button
        download_location_layout = QHBoxLayout()
        self.download_location_input = QLineEdit()
        self.download_location_input.setPlaceholderText("Set your download location...")
        self.download_location_input.setStyleSheet(
            "background-color: #444444; color: #FFFFFF; border: 1px solid #555555; padding: 8px;"
        )
        self.download_location_input.setText(self.download_location)

        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(80, 30)
        browse_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-size: 14px; 
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        browse_button.setCursor(Qt.PointingHandCursor)
        browse_button.clicked.connect(self.on_browse_clicked)

        download_location_layout.addWidget(self.download_location_input)
        download_location_layout.addWidget(browse_button)

        save_button = QPushButton("Save")
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                font-size: 14px; 
                padding: 8px 12px; 
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self.on_save_clicked)

        # Center align Save button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addStretch()

        layout.addWidget(header_label)
        layout.addWidget(download_location_label)
        layout.addLayout(download_location_layout)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_browse_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_location_input.setText(folder)

    def on_save_clicked(self):
        self.download_location = self.download_location_input.text().strip()
        if not self.download_location:
            self.download_location = QFileDialog.getExistingDirectory(self, "Please select a download folder")
        self.accept()


class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(100, 100, 600, 300)
        self.theme = "dark"  # Default theme
        self.update_theme()

        self.download_location = ""
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        settings_button = QPushButton("⚙")
        settings_button.setFixedSize(40, 40)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-size: 18px; 
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        settings_button.setCursor(Qt.PointingHandCursor)
        settings_button.clicked.connect(self.open_settings)

        theme_button = QPushButton("🌞")
        theme_button.setFixedSize(40, 40)
        theme_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                font-size: 18px; 
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        theme_button.setCursor(Qt.PointingHandCursor)
        theme_button.clicked.connect(self.toggle_theme)

        header_label = QLabel("YouTube Video Downloader")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(settings_button, 0, Qt.AlignLeft)
        header_layout.addWidget(header_label, 1)
        header_layout.addWidget(theme_button, 0, Qt.AlignRight)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste the video URL here...")
        self.url_input.setStyleSheet("background-color: #444444; color: #FFFFFF; border: 1px solid #555555; padding: 10px;")

        self.download_button = QPushButton("Start Download")
        self.download_button.setFixedSize(140, 45)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-size: 16px; 
                padding: 10px;
                border-radius: 4px;
                margin-top: 10px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.on_download_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.download_button)
        button_layout.setAlignment(Qt.AlignCenter)

        self.status_area = QWidget()
        self.status_area.setStyleSheet("""
            background-color: #444444; 
            border: 1px solid #555555; 
            padding: 10px; 
            margin-top: 10px;
            border-radius: 12px;
        """)
        status_layout = QGridLayout()
        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #F0A500;")
        self.status_label.setAlignment(Qt.AlignLeft)

        self.progress_label = QLabel("0.00 MiB/s ETA --:--")
        self.progress_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4AA8D8;")
        self.progress_label.setAlignment(Qt.AlignRight)

        self.video_title_label = QLabel("...")
        self.video_title_label.setStyleSheet("font-size: 14px; text-align: left; color: #FFFFFF;")
        self.video_title_label.setAlignment(Qt.AlignLeft)

        status_layout.addWidget(self.status_label, 0, 0, Qt.AlignLeft)
        status_layout.addWidget(self.progress_label, 0, 1, Qt.AlignRight)
        status_layout.addWidget(self.video_title_label, 1, 0, 1, 2, Qt.AlignLeft)

        self.status_area.setLayout(status_layout)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.url_input)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_area)

        self.setLayout(main_layout)

    def open_settings(self):
        settings_window = SettingsWindow(self)
        if settings_window.exec_() == QDialog.Accepted:
            self.download_location = settings_window.download_location

    def on_download_clicked(self):
        url = self.url_input.text().strip()
        if not url:
            self.update_status("Error", "Please enter a valid URL.", "0.00 MiB/s ETA --:--")
            return

        if not self.download_location:
            self.update_status("Error", "Please set a download location in settings.", "0.00 MiB/s ETA --:--")
            return

        self.update_status("Downloading...", "Fetching video info...", "0.00 MiB/s ETA --:--")
        download_video(url, self.download_location, self.update_status)

    def update_status(self, download_status, video_title, progress):
        if download_status == "Downloading...":
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
        elif download_status == "Error":
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #E57373;")
        elif download_status == "Completed":
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #81C784;")
        else:
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #F0A500;")

        self.status_label.setText(download_status)
        self.video_title_label.setText(video_title)
        self.progress_label.setText(progress)

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
        else:
            self.theme = "dark"
        self.update_theme()

    def update_theme(self):
        if self.theme == "dark":
            self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; font-family: Arial, sans-serif;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: #000000; font-family: Arial, sans-serif;")