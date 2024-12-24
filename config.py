# config.py

YDL_OPTIONS = {
    'format': 'best',  # Download the best available quality
    'outtmpl': '%(title)s.%(ext)s',  # Output template for saving the file
    'noplaylist': True,  # Prevent playlist downloading
    'quiet': True,  # Disable output logs from yt-dlp
    'extractaudio': False,  # Don't extract audio only
    'merge_output_format': 'mp4',  # Merge streams to mp4 format
    'progress_hooks': [],  # List to store the progress hooks
}