# config.py

YDL_OPTIONS = {
    'format': 'bestvideo*+bestaudio/best',  
    'outtmpl': '%(title)s.%(ext)s',  
    'noplaylist': True,  
    'quiet': True,  
    'extractaudio': False,  
    'merge_output_format': 'mp4',  
    'progress_hooks': [],
}