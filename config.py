import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Download Configuration
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', './downloads')
# Removed file size limit to allow larger files
SUPPORTED_AUDIO_FORMATS = ['mp3', 'm4a', 'opus', 'wav']
SUPPORTED_VIDEO_FORMATS = ['mp4', 'webm', 'mkv']

# Quality presets for audio
AUDIO_QUALITY_PRESETS = {
    'best': 'bestaudio/best',
    'high': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
    'medium': 'bestaudio[ext=m4a][abr<=128]/bestaudio[ext=mp3][abr<=128]/bestaudio[abr<=128]',
    'low': 'bestaudio[ext=m4a][abr<=64]/bestaudio[ext=mp3][abr<=64]/bestaudio[abr<=64]'
}

# Quality presets for video
VIDEO_QUALITY_PRESETS = {
    'best': 'best[ext=mp4]/best',
    'high': 'best[height<=1080][ext=mp4]/best[height<=1080]',
    'medium': 'best[height<=720][ext=mp4]/best[height<=720]',
    'low': 'best[height<=480][ext=mp4]/best[height<=480]'
}

# Playlist settings
MAX_PLAYLIST_ITEMS = 20  # Maximum items to process from a playlist
