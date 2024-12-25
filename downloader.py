import yt_dlp
import os
from config import YDL_OPTIONS

def create_progress_hook(update_status_callback):
    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0) / (1024 * 1024) if d.get('total_bytes') else 0
            downloaded_bytes = d.get('downloaded_bytes', 0) / (1024 * 1024) if d.get('downloaded_bytes') else 0
            percentage = (downloaded_bytes / total_bytes) * 100 if total_bytes else 0

            progress = f"{percentage:.1f}% | {total_bytes:.2f} MiB"
            video_title = d.get('info_dict', {}).get('title', 'Unknown Title')
            update_status_callback("Downloading...", video_title, progress, percentage)
        elif d['status'] == 'finished':
            update_status_callback("Completed", d['info_dict'].get('title', 'Unknown Title'), "Download Complete", 100)

    return progress_hook

def download_video_thread(url, save_path, update_status_callback):
    ydl_opts = YDL_OPTIONS.copy()
    ydl_opts['outtmpl'] = os.path.join(save_path, '%(title)s.%(ext)s')
    ydl_opts['progress_hooks'] = [create_progress_hook(update_status_callback)]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])