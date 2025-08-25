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

# Enhanced quality presets for video with 4K and 1080p support
VIDEO_QUALITY_PRESETS = {
    '4k': 'best[height>=2160][ext=mp4]/best[height>=2160]/best[ext=mp4]/best',
    '2k': 'best[height>=1440][ext=mp4]/best[height>=1440]/best[ext=mp4]/best',
    '1080p': 'best[height>=1080][ext=mp4]/best[height>=1080]/best[ext=mp4]/best',
    '720p': 'best[height>=720][ext=mp4]/best[height>=720]/best[ext=mp4]/best',
    '480p': 'best[height>=480][ext=mp4]/best[height>=480]/best[ext=mp4]/best',
    '360p': 'best[height>=360][ext=mp4]/best[height>=360]/best[ext=mp4]/best'
}

# Alternative quality presets for different use cases
VIDEO_QUALITY_ALTERNATIVES = {
    'best_quality': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'best_webm': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best',
    'best_mkv': 'bestvideo[ext=mkv]+bestaudio[ext=mkv]/best[ext=mkv]/best'
}

# Playlist settings
MAX_PLAYLIST_ITEMS = 20  # Maximum items to process from a playlist
