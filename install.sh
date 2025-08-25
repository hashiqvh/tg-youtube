#!/bin/bash

# YouTube Audio Downloader Telegram Bot - Installation Script
# This script automates the installation process on Unix-like systems

set -e

echo "🚀 Installing YouTube Audio Downloader Telegram Bot..."
echo "=================================================="

# Check if Python 3.8+ is installed
echo "🔍 Checking Python version..."
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Current version: $python_version"
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if pip is installed
echo "🔍 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip and try again."
    exit 1
fi

echo "✅ pip3 is available"

# Check if FFmpeg is installed
echo "🔍 Checking FFmpeg installation..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed. Installing FFmpeg..."
    
    # Detect OS and install FFmpeg
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "📦 Installing FFmpeg using apt..."
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            echo "📦 Installing FFmpeg using yum..."
            sudo yum install -y ffmpeg
        elif command -v dnf &> /dev/null; then
            echo "📦 Installing FFmpeg using dnf..."
            sudo dnf install -y ffmpeg
        else
            echo "❌ Could not install FFmpeg automatically. Please install it manually:"
            echo "   Ubuntu/Debian: sudo apt-get install ffmpeg"
            echo "   CentOS/RHEL: sudo yum install ffmpeg"
            echo "   Fedora: sudo dnf install ffmpeg"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "📦 Installing FFmpeg using Homebrew..."
            brew install ffmpeg
        else
            echo "❌ Homebrew is not installed. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "   Then run: brew install ffmpeg"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install FFmpeg manually."
        exit 1
    fi
else
    echo "✅ FFmpeg is already installed"
fi

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit .env file and add your Telegram bot token"
    echo "   Get your token from @BotFather on Telegram"
else
    echo "✅ .env file already exists"
fi

# Create downloads directory
echo "🔧 Creating downloads directory..."
mkdir -p downloads

# Set execute permissions
echo "🔧 Setting execute permissions..."
chmod +x bot.py
chmod +x test_bot.py

echo ""
echo "🎉 Installation completed successfully!"
echo "====================================="
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your BOT_TOKEN"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Test the installation: python test_bot.py"
echo "4. Start the bot: python bot.py"
echo ""
echo "💡 To activate the virtual environment in the future:"
echo "   source venv/bin/activate"
echo ""
echo "🔗 For help, visit the README.md file"
echo ""
echo "Happy downloading! 🎵"
