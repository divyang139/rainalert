# 🎯 STEP-BY-STEP SETUP CHECKLIST

Follow these steps in order to set up your Telegram userbot for hourly group messages.

---

## ✅ Step 1: Get Telegram API Credentials

1. [ ] Open browser and go to: https://my.telegram.org/apps
2. [ ] Sign in with your Telegram phone number
3. [ ] Enter the verification code from Telegram
4. [ ] Click **"API development tools"**
5. [ ] Fill in the form:
   - App title: `Hourly Group Sender`
   - Short name: `groupsender`
   - Platform: `Desktop`
   - Description: `Automated group message sender`
6. [ ] Click **"Create application"**
7. [ ] Copy and save these values:
   - **API ID**: (example: 12345678)
   - **API Hash**: (example: 0123456789abcdef0123456789abcdef)

**⚠️ Keep these credentials secure! Never share them.**

---

## ✅ Step 2: Prepare Your Groups

1. [ ] Make a list of 7-8 Telegram groups you want to send messages to
2. [ ] For each group, get ONE of these:
   
   **Option A: Public Group Username**
   - Open the group in Telegram
   - Check if it has a username (looks like @groupname)
   - Write it down with the @ symbol
   
   **Option B: Invite Link**
   - Open the group in Telegram
   - Tap the group name → "Invite link"
   - Copy the link (looks like https://t.me/+xxxxx)
   
3. [ ] Ensure you are a MEMBER of all these groups
4. [ ] Save your list like this:
   ```
   @group1,@group2,https://t.me/+abc123,@group4,@group5,@group6,@group7
   ```

---

## ✅ Step 3: Install Telethon Library

Open PowerShell in your project folder and run:

```powershell
pip install telethon
```

**Check if it installed:**
```powershell
pip show telethon
```

You should see version 1.24.0 or higher.

---

## ✅ Step 4: Create Configuration File

1. [ ] In your project folder, find the file: `.env.userbot.example`
2. [ ] Make a copy of it and rename to: `.env.userbot`
3. [ ] Open `.env.userbot` in a text editor
4. [ ] Fill in your details:

```env
# Replace these with your actual values:
API_ID=12345678
API_HASH=0123456789abcdef0123456789abcdef
PHONE_NUMBER=+1234567890
TARGET_GROUPS=@group1,@group2,@group3,@group4,@group5,@group6,@group7
```

**Example with real-looking data:**
```env
API_ID=15236547
API_HASH=8f2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d
PHONE_NUMBER=+919876543210
TARGET_GROUPS=@crypto_alerts,@trading_signals,https://t.me/+xYz123aBc,@market_news,@community_chat,@announcements,@general_discussion
```

5. [ ] Save and close the file

---

## ✅ Step 5: Test Your Setup

Run the test script to verify everything is configured correctly:

**PowerShell:**
```powershell
# Load environment variables
Get-Content .env.userbot | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}

# Run test
python test_userbot_setup.py
```

**What to expect:**
- ✅ "Environment variables loaded"
- ✅ "Connected as: Your Name"
- ✅ List of all your groups with green checkmarks
- ✅ "All groups accessible! You're ready to start"

**If you see errors:**
- ❌ "Missing API_ID" → Check your `.env.userbot` file
- ❌ "Cannot access group" → Make sure you're a member of that group
- ❌ Connection error → Check your internet connection

---

## ✅ Step 6: Customize Messages (Optional)

If you want to change the messages being sent:

1. [ ] Open `hourly_group_sender.py` in a text editor
2. [ ] Find the section: `MESSAGE_TEMPLATES = [`
3. [ ] Edit the messages or add your own
4. [ ] Save the file

**Example custom message:**
```python
MESSAGE_TEMPLATES = [
    """
🌟 Hello Everyone! 🌟

⏰ Current Time: {timestamp}

💬 Stay active and engaged!
📢 Check out the latest updates!

🚀 See you next hour!
""",
]
```

---

## ✅ Step 7: Start the Userbot

### Method 1: PowerShell Script (Recommended)
```powershell
.\run_userbot.ps1
```

### Method 2: Batch File
```batch
run_userbot.bat
```

### Method 3: Direct Python
```powershell
# Load environment first
Get-Content .env.userbot | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}

# Run
python hourly_group_sender.py
```

---

## ✅ Step 8: First Run Authentication

**On first run, you'll see:**

1. [ ] "Please enter your phone number:"
   - Enter with country code (e.g., +919876543210)

2. [ ] "Please enter the code you received:"
   - Check your Telegram app for a verification code
   - Enter the 5-digit code

3. [ ] If you have 2FA: "Please enter your password:"
   - Enter your Telegram password

4. [ ] "✅ Connected as: Your Name"
   - Authentication successful!

5. [ ] A file `userbot_session.session` will be created
   - Keep this file safe - you won't need to login again

---

## ✅ Step 9: Monitor Operation

Once running, you should see:

```
🚀 Starting hourly scheduler...
⏱️  Interval: Every 60 minutes
📊 Target Groups: 7

🔄 Cycle #1 - 2026-01-18 15:30:00
📤 Starting message broadcast to all groups...
📨 Sending to group 1/7...
✅ Sent to: Crypto Alerts
⏳ Waiting 5 seconds before next send...
📨 Sending to group 2/7...
✅ Sent to: Trading Signals
...
✅ Broadcast complete: 7 successful, 0 failed
⏰ Next broadcast in 60 minutes
```

---

## ✅ Step 10: Verify Messages Sent

1. [ ] Open Telegram on your phone/desktop
2. [ ] Check each of your 7-8 groups
3. [ ] You should see the message in each group
4. [ ] Wait 1 hour and check again

---

## 🎉 SUCCESS CHECKLIST

- [ ] Telethon installed
- [ ] API credentials obtained
- [ ] `.env.userbot` file created and configured
- [ ] Test script passed
- [ ] Userbot is running
- [ ] First authentication completed
- [ ] Messages sent to all groups successfully
- [ ] Logs showing no errors

---

## 🔄 Daily Operation

### To Start:
```powershell
.\run_userbot.ps1
```

### To Stop:
- Press `Ctrl + C` in the terminal

### To Check Logs:
```powershell
Get-Content userbot.log -Tail 50
```

### To Check Status:
- Look for "✅ Broadcast complete" in logs
- Verify messages in groups

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing API_ID" | Create `.env.userbot` from example file |
| "Cannot access group" | Make sure you're a member of the group |
| "Flood wait error" | Normal - bot will wait and retry |
| "Session expired" | Delete `userbot_session.session` and re-run |
| No messages sent | Check logs in `userbot.log` file |
| "Module not found" | Run `pip install telethon` |

---

## 📞 Need Help?

1. Check `userbot.log` for detailed error messages
2. Read [USERBOT_SETUP.md](USERBOT_SETUP.md) for detailed guide
3. Review [USERBOT_README.md](USERBOT_README.md) for quick reference

---

**You're all set! Your userbot will now send messages to your groups every hour automatically.** 🎉
