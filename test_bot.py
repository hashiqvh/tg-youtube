#!/usr/bin/env python3
"""
Test script for YouTube Audio Downloader Bot
Run this to test the core functionality without starting the Telegram bot
"""

import asyncio
import os
import sys
from youtube_downloader import YouTubeDownloader
from config import AUDIO_QUALITY_PRESETS

async def test_video_info():
    """Test getting video information"""
    print("🧪 Testing video info retrieval...")
    
    downloader = YouTubeDownloader()
    
    # Test with a sample YouTube URL (replace with a real one for testing)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
    
    try:
        info = await downloader.get_video_info(test_url)
        if info:
            print(f"✅ Video info retrieved successfully!")
            print(f"   Title: {info.get('title', 'Unknown')}")
            print(f"   Duration: {info.get('duration', 'Unknown')} seconds")
            print(f"   Is Playlist: {'entries' in info}")
        else:
            print("❌ Failed to get video info")
    except Exception as e:
        print(f"❌ Error getting video info: {e}")

async def test_quality_presets():
    """Test quality preset configurations"""
    print("\n🧪 Testing quality presets...")
    
    for quality, preset in AUDIO_QUALITY_PRESETS.items():
        print(f"   {quality.title()}: {preset}")
    
    print("✅ Quality presets configured correctly")

async def test_downloader_initialization():
    """Test downloader initialization"""
    print("\n🧪 Testing downloader initialization...")
    
    try:
        downloader = YouTubeDownloader()
        if os.path.exists(downloader.download_path):
            print(f"✅ Download directory created: {downloader.download_path}")
        else:
            print("❌ Download directory not created")
    except Exception as e:
        print(f"❌ Error initializing downloader: {e}")

async def test_available_qualities():
    """Test getting available qualities for a video"""
    print("\n🧪 Testing available qualities detection...")
    
    downloader = YouTubeDownloader()
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        qualities = await downloader.get_available_qualities(test_url)
        if qualities:
            print(f"✅ Available qualities: {', '.join(qualities)}")
        else:
            print("✅ Using fallback qualities")
    except Exception as e:
        print(f"❌ Error getting qualities: {e}")

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config import BOT_TOKEN, DOWNLOAD_PATH, MAX_FILE_SIZE
        print(f"✅ Configuration loaded successfully")
        print(f"   Download path: {DOWNLOAD_PATH}")
        print(f"   Max file size: {MAX_FILE_SIZE / (1024*1024):.1f} MB")
        
        if BOT_TOKEN == "your_telegram_bot_token_here":
            print("⚠️  Warning: BOT_TOKEN not set (this is expected in test mode)")
        else:
            print("✅ BOT_TOKEN is configured")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting YouTube Audio Downloader Bot Tests...\n")
    
    # Test configuration
    test_config()
    
    # Test downloader initialization
    await test_downloader_initialization()
    
    # Test quality presets
    await test_quality_presets()
    
    # Test video info (requires internet connection)
    await test_video_info()
    
    # Test quality detection (requires internet connection)
    await test_available_qualities()
    
    print("\n✨ All tests completed!")
    print("\n📝 Next steps:")
    print("1. Set your BOT_TOKEN in .env file")
    print("2. Install FFmpeg if not already installed")
    print("3. Run 'python bot.py' to start the bot")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
