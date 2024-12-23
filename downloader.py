import yt_dlp
import os
import threading
from config import YDL_OPTIONS

def create_progress_hook(update_status_callback):
    def progress_hook(d):
        if d['status'] == 'downloading':
            speed = d.get('speed', 0) / (1024 * 1024) if d.get('speed') else 0
            eta = d.get('eta', 0)
            eta_formatted = f"{eta // 60:02}:{eta % 60:02}" if eta else "--:--"
            video_title = d.get('info_dict', {}).get('title', 'Unknown Title')
            progress = f"{speed:.2f} MiB/s ETA {eta_formatted}"
            update_status_callback("Downloading...", video_title, progress)
        elif d['status'] == 'finished':
            update_status_callback("Completed", d['info_dict'].get('title', 'Unknown Title'), "Download Complete")

    return progress_hook

def download_video_thread(url, save_path, update_status_callback):
    ydl_opts = YDL_OPTIONS.copy()
    ydl_opts['outtmpl'] = os.path.join(save_path, '%(title)s.%(ext)s')
    ydl_opts['progress_hooks'] = [create_progress_hook(update_status_callback)]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            update_status_callback("Downloading...", video_title, "Starting download...")
            ydl.download([url])
    except Exception as e:
        update_status_callback("Error", f"Error: {str(e)}", "")

def download_video(url, save_path, update_status_callback):
    download_thread = threading.Thread(target=download_video_thread, args=(url, save_path, update_status_callback))
    download_thread.start()
