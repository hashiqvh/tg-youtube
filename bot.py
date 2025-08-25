import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from youtube_downloader import YouTubeDownloader
from config import BOT_TOKEN, AUDIO_QUALITY_PRESETS, VIDEO_QUALITY_PRESETS
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class YouTubeBot:
    def __init__(self):
        self.downloader = YouTubeDownloader()
        self.user_states = {}  # Store user states for multi-step interactions
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        welcome_text = """
🎵 Welcome to YouTube Downloader Bot!

I can help you download audio or video from YouTube videos and playlists.

📱 **How to use:**
• Send a YouTube URL to download
• Choose between audio or video
• Select your preferred quality
• Support for both single videos and playlists

🎬 **Video Quality Options:**
• 4K (2160p) - Ultra High Definition
• 2K (1440p) - Quad High Definition  
• 1080p - Full High Definition
• 720p - High Definition
• 480p - Standard Definition
• 360p - Low Definition

🔧 **Commands:**
/start - Show this help message
/help - Show detailed help
/quality - Set default quality
/cleanup - Clean up downloaded files

⚠️ **Note:** No file size limits - download any quality you want!
        """
        
        keyboard = [
            [InlineKeyboardButton("📚 Help", callback_data="help")],
            [InlineKeyboardButton("⚙️ Set Quality", callback_data="set_quality")],
            [InlineKeyboardButton("🧹 Cleanup", callback_data="cleanup")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send help information."""
        help_text = """
🎵 **YouTube Downloader Bot - Help**

📥 **Downloading Single Videos:**
1. Send a YouTube video URL
2. Choose between audio or video
3. Select quality (see options below)
4. Wait for download to complete
5. Receive the file

📋 **Downloading Playlists:**
1. Send a YouTube playlist URL
2. Choose between audio or video
3. Select quality
4. Bot will download up to 20 items
5. Receive multiple files

🎚️ **Audio Quality Options:**
• **Best**: Highest available quality (usually 192kbps+)
• **High**: Good quality (128kbps+)
• **Medium**: Balanced quality (64-128kbps)
• **Low**: Smaller file size (64kbps and below)

🎬 **Video Quality Options:**
• **4K (2160p)**: Ultra High Definition - Best quality available
• **2K (1440p)**: Quad High Definition - Very high quality
• **1080p**: Full High Definition - High quality, good balance
• **720p**: High Definition - Good quality, smaller files
• **480p**: Standard Definition - Medium quality, smaller files
• **360p**: Low Definition - Lower quality, smallest files

⚠️ **Limitations:**
• Maximum playlist items: 20
• Audio formats: MP3, M4A, Opus, WAV
• Video formats: MP4, WebM, MKV

🔗 **Supported URLs:**
• YouTube videos
• YouTube playlists
• YouTube Shorts
• YouTube Music

💡 **Tips:**
• Use /quality to set your preferred quality
• Use /cleanup to free up space
• For large playlists, consider downloading in smaller batches
• 4K and 2K downloads may take longer and create larger files
        """
        
        await update.message.reply_text(help_text)
    
    async def quality_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show quality selection options."""
        keyboard = []
        for quality, description in AUDIO_QUALITY_PRESETS.items():
            keyboard.append([InlineKeyboardButton(
                f"{quality.title()} Quality", 
                callback_data=f"quality_{quality}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🎚️ Select your preferred quality:",
            reply_markup=reply_markup
        )
    
    async def cleanup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clean up downloaded files."""
        try:
            self.downloader.cleanup_downloads()
            await update.message.reply_text("🧹 Download directory cleaned up successfully!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error during cleanup: {str(e)}")
    
    async def handle_youtube_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle YouTube URLs sent by users."""
        url = update.message.text.strip()
        user_id = update.effective_user.id
        
        # Check if it's a YouTube URL
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be', 'youtube.com/watch', 'youtube.com/playlist']):
            return
        
        # Send initial response
        status_message = await update.message.reply_text("🔍 Analyzing YouTube URL...")
        
        try:
            # Check if it's a playlist
            info = await self.downloader.get_video_info(url)
            if not info:
                await status_message.edit_text("❌ Could not analyze the YouTube URL. Please check if it's valid.")
                return
            
            is_playlist = 'entries' in info
            
            if is_playlist:
                playlist_title = info.get('title', 'Playlist')
                video_count = len(info.get('entries', []))
                await status_message.edit_text(
                    f"📋 **Playlist Detected:** {playlist_title}\n"
                    f"🎵 **Items:** {video_count}\n\n"
                    "What would you like to download?"
                )
            else:
                video_title = info.get('title', 'Video')
                duration = info.get('duration', 0)
                duration_str = f"{duration//60}:{duration%60:02d}" if duration > 0 else "Unknown"
                
                await status_message.edit_text(
                    f"🎵 **Video:** {video_title}\n"
                    f"⏱️ **Duration:** {duration_str}\n\n"
                    "What would you like to download?"
                )
            
            # Store user state
            self.user_states[user_id] = {
                'url': url,
                'is_playlist': is_playlist,
                'info': info
            }
            
            # Show download type selection
            keyboard = [
                [InlineKeyboardButton("🎵 Audio Only", callback_data=f"type_audio_{user_id}")],
                [InlineKeyboardButton("🎬 Video", callback_data=f"type_video_{user_id}")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await status_message.edit_text(
                status_message.text + "\n\n📥 **Select Download Type:**",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Error handling URL: {e}")
            await status_message.edit_text(f"❌ Error analyzing URL: {str(e)}")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "help":
            await self.help_command(update, context)
        elif data == "set_quality":
            await self.quality_command(update, context)
        elif data == "cleanup":
            await self.cleanup_command(update, context)
        elif data.startswith("quality_"):
            quality = data.split("_")[1]
            await query.edit_message_text(f"✅ Default quality set to: **{quality.title()}**")
        elif data.startswith("type_"):
            await self.handle_type_selection(query, data)
        elif data.startswith("download_"):
            await self.handle_download_callback(query, data)
    
    async def handle_type_selection(self, query, data):
        """Handle download type selection (audio/video)."""
        try:
            parts = data.split("_")
            download_type = parts[1]  # audio or video
            user_id = int(parts[2])
            
            if user_id not in self.user_states:
                await query.edit_message_text("❌ Session expired. Please send the URL again.")
                return
            
            user_state = self.user_states[user_id]
            user_state['download_type'] = download_type
            
            # Show quality selection
            if download_type == 'audio':
                quality_presets = AUDIO_QUALITY_PRESETS
                type_text = "🎵 Audio"
            else:
                quality_presets = VIDEO_QUALITY_PRESETS
                type_text = "🎬 Video"
            
            # Create keyboard with quality options
            keyboard = []
            row = []
            for i, (quality, description) in enumerate(quality_presets.items()):
                # Create quality labels with resolution info
                if download_type == 'video':
                    if quality == '4k':
                        label = "4K (2160p)"
                    elif quality == '2k':
                        label = "2K (1440p)"
                    elif quality == '1080p':
                        label = "1080p (FHD)"
                    elif quality == '720p':
                        label = "720p (HD)"
                    elif quality == '480p':
                        label = "480p (SD)"
                    elif quality == '360p':
                        label = "360p (LD)"
                    else:
                        label = f"{quality.title()}"
                else:
                    label = f"{quality.title()}"
                
                row.append(InlineKeyboardButton(
                    label, 
                    callback_data=f"download_{download_type}_{quality}_{user_id}"
                ))
                
                # Create new row every 2 buttons for better layout
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
            
            # Add remaining buttons if any
            if row:
                keyboard.append(row)
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"{type_text} download selected!\n\n"
                "🎚️ **Select Quality:**",
                reply_markup=reply_markup
            )
                
        except Exception as e:
            logger.error(f"Error handling type selection: {e}")
            await query.edit_message_text(f"❌ Error during type selection: {str(e)}")
    
    async def handle_download_callback(self, query, data):
        """Handle download quality selection."""
        try:
            parts = data.split("_")
            download_type = parts[1]  # audio or video
            quality = parts[2]
            user_id = int(parts[3])
            
            if user_id not in self.user_states:
                await query.edit_message_text("❌ Session expired. Please send the URL again.")
                return
            
            user_state = self.user_states[user_id]
            url = user_state['url']
            is_playlist = user_state['is_playlist']
            
            # Create quality display text
            if download_type == 'video':
                quality_display = {
                    '4k': '4K (2160p)',
                    '2k': '2K (1440p)',
                    '1080p': '1080p (FHD)',
                    '720p': '720p (HD)',
                    '480p': '480p (SD)',
                    '360p': '360p (LD)'
                }.get(quality, quality.title())
            else:
                quality_display = quality.title()
            
            # Update status message
            type_text = "🎵 Audio" if download_type == 'audio' else "🎬 Video"
            await query.edit_message_text(
                f"⏳ Downloading {type_text} with {quality_display} quality...\n"
                f"Please wait, this may take a while."
            )
            
            if is_playlist:
                await self.download_playlist_for_user(query, url, download_type, quality, user_id)
            else:
                await self.download_single_video_for_user(query, url, download_type, quality, user_id)
                
        except Exception as e:
            logger.error(f"Error handling download callback: {e}")
            await query.edit_message_text(f"❌ Error during download: {str(e)}")
    
    async def download_single_video_for_user(self, query, url, download_type, quality, user_id):
        """Download a single video for a user."""
        try:
            file_path = await self.downloader.download_single_video(url, download_type, quality)
            
            if file_path and os.path.exists(file_path):
                if download_type == 'audio':
                    # Send the audio file
                    with open(file_path, 'rb') as audio_file:
                        await query.message.reply_audio(
                            audio_file,
                            title=os.path.basename(file_path).replace('.mp3', ''),
                            performer="YouTube Audio"
                        )
                else:
                    # Send the video file
                    with open(file_path, 'rb') as video_file:
                        await query.message.reply_video(
                            video_file,
                            caption=f"YouTube Video - {quality.upper()} Quality"
                        )
                
                # Clean up the file
                os.remove(file_path)
                
                type_text = "Audio" if download_type == 'audio' else "Video"
                await query.edit_message_text(f"✅ {type_text} download completed successfully!")
            else:
                await query.edit_message_text("❌ Download failed. Please try again.")
                
        except Exception as e:
            logger.error(f"Error downloading single video: {e}")
            await query.edit_message_text(f"❌ Download error: {str(e)}")
        finally:
            # Clean up user state
            if user_id in self.user_states:
                del self.user_states[user_id]
    
    async def download_playlist_for_user(self, query, url, download_type, quality, user_id):
        """Download a playlist for a user."""
        try:
            downloaded_files = await self.downloader.download_playlist(url, download_type, quality)
            
            if downloaded_files:
                type_text = "Audio" if download_type == 'audio' else "Video"
                await query.edit_message_text(f"✅ Downloaded {len(downloaded_files)} {type_text.lower()} files!")
                
                # Send each file
                for i, file_path in enumerate(downloaded_files):
                    if os.path.exists(file_path):
                        try:
                            if download_type == 'audio':
                                with open(file_path, 'rb') as audio_file:
                                    await query.message.reply_audio(
                                        audio_file,
                                        title=f"{i+1:02d}_{os.path.basename(file_path).replace('.mp3', '')}",
                                        performer="YouTube Playlist"
                                    )
                            else:
                                with open(file_path, 'rb') as video_file:
                                    await query.message.reply_video(
                                        video_file,
                                        caption=f"{i+1:02d} - YouTube Playlist - {quality.upper()} Quality"
                                    )
                            
                            # Clean up the file
                            os.remove(file_path)
                            
                            # Small delay to avoid flooding
                            await asyncio.sleep(0.5)
                            
                        except Exception as e:
                            logger.error(f"Error sending playlist file {file_path}: {e}")
                            continue
                
                await query.message.reply_text(f"🎉 Playlist {type_text.lower()} download completed!")
            else:
                await query.edit_message_text("❌ Playlist download failed. Please try again.")
                
        except Exception as e:
            logger.error(f"Error downloading playlist: {e}")
            await query.edit_message_text(f"❌ Playlist download error: {str(e)}")
        finally:
            # Clean up user state
            if user_id in self.user_states:
                del self.user_states[user_id]
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)
    
    def run(self):
        """Start the bot."""
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("quality", self.quality_command))
        application.add_handler(CommandHandler("cleanup", self.cleanup_command))
        
        # Handle YouTube URLs
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_youtube_url))
        
        # Handle button callbacks
        application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Handle errors
        application.add_error_handler(self.error_handler)
        
        # Start the bot
        logger.info("Starting YouTube Downloader Bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot."""
    bot = YouTubeBot()
    bot.run()

if __name__ == '__main__':
    main()
