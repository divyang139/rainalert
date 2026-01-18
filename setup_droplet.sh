#!/bin/bash

# DigitalOcean Droplet Setup Script for Telethon Rain Monitor
# Run this after creating your Ubuntu droplet

echo "🚀 Setting up Telethon Rain Monitor on DigitalOcean..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
echo "🐍 Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/telegram-monitor
cd /opt/telegram-monitor

# Upload your files here or clone from git
echo "⬆️  Upload your files to /opt/telegram-monitor/"
echo "   Files needed:"
echo "   - telethon_nigeria_monitor.py"
echo "   - scheduled_group_sender.py (optional)"
echo "   - requirements.txt"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install telethon

# Create .env file
echo "⚙️  Creating environment file..."
sudo tee /opt/telegram-monitor/.env > /dev/null <<EOF
API_ID=your_api_id_here
API_HASH=your_api_hash_here
SOURCE_CHANNEL=RainAnalytics
TARGET_CHANNEL=your_target_channel
TARGET_GROUPS=group1,group2,group3
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit /opt/telegram-monitor/.env with your credentials:"
echo "   sudo nano /opt/telegram-monitor/.env"
echo ""
echo "2. Upload your Python scripts to /opt/telegram-monitor/"
echo ""
echo "3. Run initial setup (authenticate with Telegram):"
echo "   cd /opt/telegram-monitor"
echo "   source venv/bin/activate"
echo "   python3 telethon_nigeria_monitor.py"
echo ""
echo "4. After authentication, press Ctrl+C and set up systemd service"
echo "   See DEPLOYMENT.md for systemd setup instructions"
