# DigitalOcean Droplet Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Create DigitalOcean Droplet

1. Go to [DigitalOcean](https://www.digitalocean.com/)
2. Use your **GitHub Student Pack** to activate $200 credit
3. Create a new Droplet:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic $4/month (512MB RAM is enough)
   - **Region**: Choose closest to you
   - **Authentication**: SSH key (recommended) or password
4. Wait for droplet creation

### 2. Connect to Your Droplet

```bash
ssh root@your_droplet_ip
```

### 3. Upload Files to Droplet

**Option A: Using SCP (from your local machine)**
```bash
scp telethon_nigeria_monitor.py root@your_droplet_ip:/opt/telegram-monitor/
scp scheduled_group_sender.py root@your_droplet_ip:/opt/telegram-monitor/
scp telegram-monitor.service root@your_droplet_ip:/tmp/
```

**Option B: Using Git (recommended)**
```bash
# On droplet
cd /opt
git clone https://github.com/yourusername/yourrepo.git telegram-monitor
cd telegram-monitor
```

### 4. Run Setup Script

```bash
# On droplet
cd /opt/telegram-monitor
bash setup_droplet.sh
```

### 5. Configure Environment Variables

```bash
nano /opt/telegram-monitor/.env
```

Edit the file:
```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
SOURCE_CHANNEL=RainAnalytics
TARGET_CHANNEL=yourchannelname
TARGET_GROUPS=https://t.me/+link1,https://t.me/+link2
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### 6. First Run (Authentication)

```bash
cd /opt/telegram-monitor
source venv/bin/activate
python3 telethon_nigeria_monitor.py
```

- Enter your phone number when prompted
- Enter the code sent to your Telegram
- Enter 2FA password if enabled
- After successful login, press `Ctrl+C`

### 7. Set Up Systemd Service (Run 24/7)

```bash
# Copy service file
sudo cp /opt/telegram-monitor/telegram-monitor.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable telegram-monitor

# Start service
sudo systemctl start telegram-monitor

# Check status
sudo systemctl status telegram-monitor
```

### 8. Verify It's Running

```bash
# View logs
sudo journalctl -u telegram-monitor -f

# Check if process is running
ps aux | grep telethon
```

## 🔧 Useful Commands

### Check logs
```bash
sudo journalctl -u telegram-monitor -f
```

### Restart service
```bash
sudo systemctl restart telegram-monitor
```

### Stop service
```bash
sudo systemctl stop telegram-monitor
```

### View service status
```bash
sudo systemctl status telegram-monitor
```

### Update script
```bash
cd /opt/telegram-monitor
# Edit your script
nano telethon_nigeria_monitor.py
# Restart service
sudo systemctl restart telegram-monitor
```

## 🎯 Optional: Run Scheduled Sender Too

Create second service for scheduled messages:

```bash
# Create service file
sudo nano /etc/systemd/system/telegram-scheduler.service
```

Paste:
```ini
[Unit]
Description=Telethon Scheduled Group Sender
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/telegram-monitor
Environment="PATH=/opt/telegram-monitor/venv/bin"
EnvironmentFile=/opt/telegram-monitor/.env
ExecStart=/opt/telegram-monitor/venv/bin/python3 /opt/telegram-monitor/scheduled_group_sender.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-scheduler
sudo systemctl start telegram-scheduler
sudo systemctl status telegram-scheduler
```

## 🛡️ Security Tips

1. **Firewall Setup**
```bash
sudo ufw allow ssh
sudo ufw enable
```

2. **Keep System Updated**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Monitor Disk Space**
```bash
df -h
```

## 💰 Cost

- **$4/month droplet** = 50 months free with $200 credit
- Your script will run 24/7 without interruption

## 📊 Monitor Usage

```bash
# Check RAM usage
free -h

# Check CPU usage
top

# Check logs size
du -sh /var/log/
```

## 🆘 Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u telegram-monitor -n 50

# Check file permissions
ls -la /opt/telegram-monitor/
```

### Script errors
```bash
# Run manually to see errors
cd /opt/telegram-monitor
source venv/bin/activate
python3 telethon_nigeria_monitor.py
```

### Session issues
```bash
# Delete session and re-authenticate
rm /opt/telegram-monitor/*.session
# Then run first-time setup again
```

## ✅ Done!

Your Telegram monitor is now running 24/7 on DigitalOcean! 🎉
