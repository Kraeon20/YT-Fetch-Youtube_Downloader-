# config.py
import os
import sys

if getattr(sys, 'frozen', False):  
    FFMPEG_PATH = os.path.join(sys._MEIPASS, 'ffmpeg', 'ffmpeg')
else:  
    FFMPEG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ffmpeg', 'ffmpeg')

YDL_OPTIONS = {
    'format': 'bestvideo*+bestaudio/best',  
    'outtmpl': '%(title)s.%(ext)s',  
    'noplaylist': True,  
    'quiet': True,  
    'extractaudio': False,  
    'merge_output_format': 'mp4',  
    'progress_hooks': [],
    'ffmpeg_location': FFMPEG_PATH,
}