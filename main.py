import sys
from PyQt5.QtWidgets import QApplication
from ui import YouTubeDownloaderApp

def main():
    app = QApplication(sys.argv)
    downloader_ui = YouTubeDownloaderApp()
    downloader_ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    