import os
import asyncio
import yt_dlp
from typing import Dict, List, Optional, Tuple
import logging
from config import DOWNLOAD_PATH, AUDIO_QUALITY_PRESETS, VIDEO_QUALITY_PRESETS, MAX_PLAYLIST_ITEMS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self):
        self.download_path = DOWNLOAD_PATH
        os.makedirs(self.download_path, exist_ok=True)
        
    def _get_ydl_opts(self, download_type: str = 'audio', quality: str = 'best', output_template: str = '%(title)s.%(ext)s') -> Dict:
        """Get yt-dlp options for audio or video download"""
        if download_type == 'audio':
            quality_format = AUDIO_QUALITY_PRESETS.get(quality, AUDIO_QUALITY_PRESETS['best'])
            return {
                'format': quality_format,
                'outtmpl': os.path.join(self.download_path, output_template),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
                'no_warnings': True,
                'quiet': True,
            }
        else:  # video
            quality_format = VIDEO_QUALITY_PRESETS.get(quality, VIDEO_QUALITY_PRESETS['best'])
            return {
                'format': quality_format,
                'outtmpl': os.path.join(self.download_path, output_template),
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
                'no_warnings': True,
                'quiet': True,
            }
    
    async def get_video_info(self, url: str) -> Optional[Dict]:
        """Get video information without downloading"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    async def download_single_video(self, url: str, download_type: str = 'audio', quality: str = 'best') -> Optional[str]:
        """Download a single video as audio or video"""
        try:
            # Get video info first
            info = await self.get_video_info(url)
            if not info:
                return None
            
            # Check if it's a playlist
            if 'entries' in info:
                logger.warning("URL contains playlist, use download_playlist instead")
                return None
            
            # Create output template with safe filename
            safe_title = "".join(c for c in info.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            if download_type == 'audio':
                output_template = f"{safe_title}.%(ext)s"
                expected_extension = '.mp3'
            else:
                output_template = f"{safe_title}.%(ext)s"
                expected_extension = '.mp4'
            
            ydl_opts = self._get_ydl_opts(download_type, quality, output_template)
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the downloaded file
            for file in os.listdir(self.download_path):
                if file.startswith(safe_title) and file.endswith(expected_extension):
                    file_path = os.path.join(self.download_path, file)
                    return file_path
            
            return None
            
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None
    
    async def download_playlist(self, url: str, download_type: str = 'audio', quality: str = 'best', max_items: int = None) -> List[str]:
        """Download multiple videos from a playlist"""
        try:
            if max_items is None:
                max_items = MAX_PLAYLIST_ITEMS
            
            # Get playlist info
            info = await self.get_video_info(url)
            if not info or 'entries' not in info:
                logger.error("URL is not a playlist")
                return []
            
            entries = info['entries'][:max_items]
            downloaded_files = []
            
            for i, entry in enumerate(entries):
                if not entry:
                    continue
                
                try:
                    video_url = entry.get('url') or entry.get('webpage_url')
                    if not video_url:
                        continue
                    
                    # Create output template with index and safe filename
                    safe_title = "".join(c for c in entry.get('title', f'video_{i+1}') if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    
                    if download_type == 'audio':
                        output_template = f"{i+1:02d}_{safe_title}.%(ext)s"
                        expected_extension = '.mp3'
                    else:
                        output_template = f"{i+1:02d}_{safe_title}.%(ext)s"
                        expected_extension = '.mp4'
                    
                    ydl_opts = self._get_ydl_opts(download_type, quality, output_template)
                    
                    # Download the video
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    # Find the downloaded file
                    for file in os.listdir(self.download_path):
                        if file.startswith(f"{i+1:02d}_{safe_title}") and file.endswith(expected_extension):
                            file_path = os.path.join(self.download_path, file)
                            downloaded_files.append(file_path)
                    
                    # Small delay to avoid overwhelming the server
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error downloading playlist item {i+1}: {e}")
                    continue
            
            return downloaded_files
            
        except Exception as e:
            logger.error(f"Error downloading playlist: {e}")
            return []
    
    async def get_available_qualities(self, url: str, download_type: str = 'audio') -> List[str]:
        """Get available quality options for a video"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:
                    # It's a playlist, get info from first video
                    if info['entries']:
                        info = info['entries'][0]
                    else:
                        return []
                
                if download_type == 'audio':
                    formats = info.get('formats', [])
                    audio_formats = [f for f in formats if f.get('acodec') != 'none']
                    
                    qualities = []
                    for fmt in audio_formats:
                        abr = fmt.get('abr', 0)
                        if abr > 0:
                            if abr >= 192:
                                qualities.append('best')
                            elif abr >= 128:
                                qualities.append('high')
                            elif abr >= 64:
                                qualities.append('medium')
                            else:
                                qualities.append('low')
                else:  # video
                    formats = info.get('formats', [])
                    video_formats = [f for f in formats if f.get('vcodec') != 'none']
                    
                    qualities = []
                    for fmt in video_formats:
                        height = fmt.get('height', 0)
                        if height > 0:
                            if height >= 1080:
                                qualities.append('best')
                            elif height >= 720:
                                qualities.append('high')
                            elif height >= 480:
                                qualities.append('medium')
                            else:
                                qualities.append('low')
                
                return list(set(qualities))  # Remove duplicates
                
        except Exception as e:
            logger.error(f"Error getting available qualities: {e}")
            if download_type == 'audio':
                return ['best', 'high', 'medium', 'low']  # Fallback to default audio qualities
            else:
                return ['best', 'high', 'medium', 'low']  # Fallback to default video qualities
    
    def cleanup_downloads(self):
        """Clean up downloaded files"""
        try:
            for file in os.listdir(self.download_path):
                file_path = os.path.join(self.download_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            logger.info("Download directory cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up downloads: {e}")
