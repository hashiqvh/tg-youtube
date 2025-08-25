# YouTube Downloader Telegram Bot

A powerful Telegram bot that downloads audio or video from YouTube videos and playlists with quality selection options, including **4K, 2K, and 1080p** support.

## Features

🎵 **Audio Downloads**: Convert YouTube videos to high-quality audio files
🎬 **Video Downloads**: Download YouTube videos in various qualities including **4K Ultra HD**
📋 **Playlist Support**: Download entire playlists (up to 20 videos)
🎚️ **Quality Selection**: Choose from best, high, medium, or low quality
📱 **User-Friendly**: Interactive buttons and clear status updates
🧹 **Auto-Cleanup**: Files are automatically removed after sending
⚡ **Fast Processing**: Efficient downloading with yt-dlp
🚫 **No File Limits**: Download any quality without size restrictions
🆕 **4K Support**: Download videos in Ultra High Definition (2160p)

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- Telegram Bot Token from @BotFather

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd youtube-tg
   ```

2. **Install Python dependencies:**
   ```bash
   ./install.sh
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file and add your Telegram bot token:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   DOWNLOAD_PATH=./downloads
   ```

## Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided by BotFather
5. Paste it in your `.env` file

## Usage

### Starting the Bot

```bash
python bot.py
```

### Bot Commands

- `/start` - Show welcome message and main menu
- `/help` - Display detailed help information
- `/quality` - Set default quality preference
- `/cleanup` - Clean up downloaded files

### Downloading Content

1. **Single Video:**
   - Send a YouTube video URL to the bot
   - Choose between **Audio Only** or **Video**
   - Choose your preferred quality
   - Wait for download to complete
   - Receive the file

2. **Playlist:**
   - Send a YouTube playlist URL to the bot
   - Choose between **Audio Only** or **Video**
   - Choose quality
   - Bot downloads up to 20 items
   - Receive multiple files

### Quality Options

#### 🎵 **Audio Quality:**
- **Best**: Highest available quality (usually 192kbps+)
- **High**: Good quality (128kbps+)
- **Medium**: Balanced quality (64-128kbps)
- **Low**: Smaller file size (64kbps and below)

#### 🎬 **Video Quality (NEW!):**
- **4K (2160p)**: Ultra High Definition - Best quality available
- **2K (1440p)**: Quad High Definition - Very high quality  
- **1080p**: Full High Definition - High quality, good balance
- **720p**: High Definition - Good quality, smaller files
- **480p**: Standard Definition - Medium quality, smaller files
- **360p**: Low Definition - Lower quality, smallest files

## Supported URLs

- YouTube videos
- YouTube playlists
- YouTube Shorts
- YouTube Music

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Your Telegram bot token | Required |
| `DOWNLOAD_PATH` | Directory for temporary files | `./downloads` |

### Quality Presets

You can modify the quality presets in `config.py`:

```python
# Audio quality presets
AUDIO_QUALITY_PRESETS = {
    'best': 'bestaudio/best',
    'high': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
    'medium': 'bestaudio[ext=m4a][abr<=128]/bestaudio[ext=mp3][abr<=128]/bestaudio[abr<=128]',
    'low': 'bestaudio[ext=m4a][abr<=64]/bestaudio[ext=mp3][abr<=64]/bestaudio[abr<=64]'
}

# Enhanced video quality presets with 4K support
VIDEO_QUALITY_PRESETS = {
    '4k': 'best[height>=2160][ext=mp4]/best[height>=2160]/best[ext=mp4]/best',
    '2k': 'best[height>=1440][ext=mp4]/best[height>=1440]/best[ext=mp4]/best',
    '1080p': 'best[height>=1080][ext=mp4]/best[height>=1080]/best[ext=mp4]/best',
    '720p': 'best[height>=720][ext=mp4]/best[height>=720]/best[ext=mp4]/best',
    '480p': 'best[height>=480][ext=mp4]/best[height>=480]/best[ext=mp4]/best',
    '360p': 'best[height>=360][ext=mp4]/best[height>=360]/best[ext=mp4]/best'
}
```

## Limitations

- **Playlist Items**: Maximum 20 videos per playlist
- **Audio Formats**: Outputs MP3 format for compatibility
- **Video Formats**: MP4, WebM, MKV
- **Rate Limiting**: Built-in delays to avoid overwhelming servers
- **File Size**: Telegram has a 2GB file size limit

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error:**
   - Ensure FFmpeg is installed and in your system PATH
   - Restart your terminal after installation

2. **"Bot token invalid" error:**
   - Check your `.env` file has the correct token
   - Verify the token with @BotFather

3. **Download fails:**
   - Check internet connection
   - Verify YouTube URL is accessible
   - Try with a different quality setting

4. **Large file issues:**
   - Telegram has a 2GB file size limit
   - Use lower quality settings for very long videos
   - Consider downloading in parts for extremely long content

5. **4K/2K download issues:**
   - Ensure you have sufficient bandwidth
   - 4K downloads may take significantly longer
   - Some videos may not have 4K quality available

### Logs

The bot provides detailed logging. Check the console output for error messages and debugging information.

## Security Considerations

- Keep your bot token private
- Don't share your `.env` file
- The bot only processes YouTube URLs
- Downloaded files are automatically cleaned up

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader library
- [FFmpeg](https://ffmpeg.org/) - Audio/Video processing

## Support

If you encounter issues:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all prerequisites are met
4. Open an issue on GitHub with detailed information

---

**Note**: This bot is for personal use only. Please respect YouTube's terms of service and copyright laws.
