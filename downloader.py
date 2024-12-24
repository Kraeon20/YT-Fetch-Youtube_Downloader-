import yt_dlp
import os
import threading
from config import YDL_OPTIONS

def create_progress_hook(update_status_callback):
    def progress_hook(d):
        if d['status'] == 'downloading':
            # Handle download progress, showing speed and ETA
            speed = d.get('speed', 0) / (1024 * 1024) if d.get('speed') else 0
            eta = d.get('eta', 0)
            eta_formatted = f"{eta // 60:02}:{eta % 60:02}" if eta else "--:--"
            video_title = d.get('info_dict', {}).get('title', 'Unknown Title')
            progress = f"{speed:.2f} MiB/s ETA {eta_formatted}"
            update_status_callback("Downloading...", video_title, progress)
        elif d['status'] == 'finished':
            # Handle completion status
            update_status_callback("Completed", d['info_dict'].get('title', 'Unknown Title'), "Download Complete")

    return progress_hook

def download_video_thread(url, save_path, update_status_callback):
    # Prepare yt-dlp options
    ydl_opts = YDL_OPTIONS.copy()
    ydl_opts['outtmpl'] = os.path.join(save_path, '%(title)s.%(ext)s')

    def progress_hook(d):
        if d['status'] == 'downloading':
            total_size = d.get('total_bytes', 0)
            downloaded = d.get('downloaded_bytes', 0)
            percentage = (downloaded / total_size) * 100 if total_size else 0.0
            
            speed = d.get('speed', 0) / (1024 * 1024) if d.get('speed') else 0.0
            eta = d.get('eta', 0)
            eta_formatted = f"{eta // 60:02}:{eta % 60:02}" if eta else "--:--"
            
            video_title = d.get('info_dict', {}).get('title', 'Unknown Title')
            progress = f"{speed:.2f} MiB/s ETA {eta_formatted}"
            update_status_callback("Downloading...", video_title, progress, percentage)
        
        elif d['status'] == 'finished':
            video_title = d.get('info_dict', {}).get('title', 'Unknown Title')
            update_status_callback("Completed", video_title, "Download Complete", 100.0)

    ydl_opts['progress_hooks'] = [progress_hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Inform UI of the starting status
            update_status_callback("Starting", "Initializing...", "Preparing to download", 0.0)
            
            # Extract and display video info before downloading
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            update_status_callback("Downloading...", video_title, "Starting download...", 0.0)
            
            # Start the actual download
            ydl.download([url])
    except Exception as e:
        # Report any errors back to the UI
        update_status_callback("Error", f"Error: {str(e)}", "", 0.0)

def download_video(url, save_path, update_status_callback):
    # Start the download in a separate thread
    download_thread = threading.Thread(target=download_video_thread, args=(url, save_path, update_status_callback))
    download_thread.daemon = True  # Ensure the thread exits when the main program ends
    download_thread.start()