# 🤖 Telegram Hourly Group Message Userbot

Automatically sends scheduled messages to 7-8 Telegram groups every hour.

---

## ⚡ Quick Start (5 Minutes)

### 1️⃣ Install Dependencies
```bash
pip install telethon
```

### 2️⃣ Get Telegram API Credentials
- Go to https://my.telegram.org/apps
- Login and create an app
- Copy your **API ID** and **API Hash**

### 3️⃣ Configure Settings
```bash
# Copy the example file
copy .env.userbot.example .env.userbot

# Edit .env.userbot with your details:
API_ID=12345678
API_HASH=your_api_hash_here
PHONE_NUMBER=+1234567890
TARGET_GROUPS=@group1,@group2,@group3,@group4,@group5,@group6,@group7,@group8
```

### 4️⃣ Test Your Setup
```powershell
# Load environment and test
Get-Content .env.userbot | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}
python test_userbot_setup.py
```

### 5️⃣ Run the Userbot
```powershell
.\run_userbot.ps1
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `hourly_group_sender.py` | Main userbot script |
| `run_userbot.ps1` | PowerShell launcher script |
| `test_userbot_setup.py` | Test connection and groups |
| `.env.userbot.example` | Configuration template |
| `USERBOT_SETUP.md` | Detailed setup guide |

---

## 🎯 Features

✅ Sends messages to 7-8+ groups automatically  
✅ Configurable interval (default: every hour)  
✅ Multiple rotating message templates  
✅ Custom messages per group  
✅ Auto-joins groups via invite links  
✅ Flood protection & error handling  
✅ Detailed logging to `userbot.log`  
✅ Session persistence (login once)  

---

## ⚙️ Customization

### Change Sending Interval
Edit `hourly_group_sender.py`:
```python
SEND_INTERVAL = 3600  # 1 hour in seconds

# Examples:
# 30 minutes: 1800
# 2 hours: 7200
# 6 hours: 21600
```

### Customize Messages
Edit the `MESSAGE_TEMPLATES` list in `hourly_group_sender.py`:
```python
MESSAGE_TEMPLATES = [
    """
🌟 Your Custom Message 🌟
⏰ Time: {timestamp}
Your content here!
""",
]
```

### Different Messages for Different Groups
```python
CUSTOM_GROUP_MESSAGES = {
    "@group1": "Special message for group 1: {timestamp}",
    "@group2": "Different message for group 2: {timestamp}",
}
```

---

## 🔧 Common Issues

**"Missing API credentials"**  
→ Create `.env.userbot` from `.env.userbot.example` and fill in your details

**"Cannot access group"**  
→ Make sure you're a member of the group first

**"Flood wait error"**  
→ Increase `DELAY_BETWEEN_GROUPS` in the script (default: 5 seconds)

**"Session expired"**  
→ Delete `userbot_session.session` file and run again to re-login

---

## 📊 Monitoring

Check logs in real-time:
```powershell
Get-Content userbot.log -Wait -Tail 50
```

View last 20 lines:
```powershell
Get-Content userbot.log -Tail 20
```

---

## 🛑 Stopping the Userbot

Press `Ctrl + C` in the terminal running the bot

---

## 📚 More Information

See [USERBOT_SETUP.md](USERBOT_SETUP.md) for detailed documentation including:
- Advanced configuration
- Running as a background service
- Security best practices
- Troubleshooting guide

---

## ⚠️ Important Notes

- Use responsibly and follow Telegram's Terms of Service
- Don't spam or send unsolicited messages
- Respect group rules and admin guidelines
- Keep your API credentials secure
- Never share your session file

---

## 💡 Tips

1. **Test with 2-3 groups first** before adding all 7-8 groups
2. **Monitor the first few cycles** to ensure everything works
3. **Check logs regularly** for any issues
4. **Keep backups** of your session file
5. **Use 2FA** on your Telegram account for security

---

## 🎯 Example Group Formats

```env
# Public groups (with @)
TARGET_GROUPS=@cryptotrading,@technews,@community

# Invite links
TARGET_GROUPS=https://t.me/+abc123xyz,https://t.me/+def456uvw

# Mixed
TARGET_GROUPS=@public_group,https://t.me/+private_link,@another_group

# 7-8 groups example
TARGET_GROUPS=@group1,@group2,@group3,https://t.me/+link1,https://t.me/+link2,@group6,@group7,@group8
```

---

**Ready to start?** Run `.\run_userbot.ps1` and watch it work! 🚀
