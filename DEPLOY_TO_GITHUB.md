# 🚀 Quick Deploy to GitHub Actions

## 🎯 One-Time Setup (5 minutes)

### 1️⃣ Generate Session Locally
```bash
python generate_session.py
```

### 2️⃣ Convert Session to Base64
```bash
python convert_session_to_base64.py
```
**Save the output** - you'll need it for GitHub!

### 3️⃣ Create GitHub Repository
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Add scheduled userbot"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 4️⃣ Add GitHub Secrets

Go to: **Your Repo → Settings → Secrets and variables → Actions**

Add these 4 secrets:

| Secret Name | Where to Get It | Example |
|------------|----------------|---------|
| `TELEGRAM_API_ID` | https://my.telegram.org | `12345678` |
| `TELEGRAM_API_HASH` | https://my.telegram.org | `abcdef123456` |
| `TELEGRAM_PHONE` | Your phone number | `+1234567890` |
| `SESSION_STRING` | Output from step 2 | Base64 string |

### 5️⃣ Test It!

1. Go to **Actions** tab
2. Click **Scheduled Userbot Messages**
3. Click **Run workflow** → **Run workflow**
4. Wait 1-2 minutes
5. Check logs ✅

---

## ⚙️ Schedule Configuration

The bot runs **every hour** by default. To change:

Edit [.github/workflows/scheduled_userbot.yml](.github/workflows/scheduled_userbot.yml#L5):

```yaml
# Current: Every hour
- cron: '0 * * * *'

# Every 30 minutes
- cron: '*/30 * * * *'

# Every 2 hours
- cron: '0 */2 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Every day at 9 AM UTC
- cron: '0 9 * * *'

# Monday to Friday at 9 AM UTC
- cron: '0 9 * * 1-5'
```

---

## 📝 Customize Messages

Edit [scheduled_group_sender.py](scheduled_group_sender.py):

```python
# Line 13-20: Your group chat IDs
GROUP_CHAT_IDS = [
    -1001234567890,  # Group 1
    -1009876543210,  # Group 2
    # Add more...
]

# Line 23-30: Your messages
MESSAGES = [
    "Hello everyone! 👋",
    "Good morning! ☀️",
    # Add more...
]
```

---

## 🔍 How to Find Group Chat IDs

### Method 1: Use the test script
```bash
python test_userbot_setup.py
```

### Method 2: Manual check
1. Forward a message from the group to https://t.me/userinfobot
2. It will show the chat ID

---

## 📊 Monitor Your Bot

### Check Workflow Runs
- Go to **Actions** tab
- See all runs with timestamps
- ✅ Green = Success
- ❌ Red = Failed

### View Logs
1. Click on any run
2. Click **send-messages** job
3. Expand steps to see detailed logs

### GitHub Actions Usage
- Free tier: 2,000 minutes/month (private repos)
- Public repos: Unlimited
- Each run: ~1-2 minutes
- Hourly schedule: ~720 minutes/month ✅

---

## 🐛 Common Issues

### "Session file not found"
- Make sure you added `SESSION_STRING` secret
- Verify the base64 string is complete

### "API ID invalid"
- Check `TELEGRAM_API_ID` secret
- Must be a number (no quotes in GitHub Secret)

### "Phone number invalid"
- Check `TELEGRAM_PHONE` secret
- Include country code: `+1234567890`

### "Flood wait error"
- Telegram rate limiting
- Add delays between messages
- Reduce frequency

---

## 🔒 Security Checklist

- ✅ Never commit session files
- ✅ Use GitHub Secrets for credentials
- ✅ Keep repository private (optional)
- ✅ Enable 2FA on GitHub
- ✅ Review Actions logs regularly

---

## 💡 Pro Tips

1. **Test locally first** before deploying to GitHub
2. **Start with manual triggers** before enabling schedule
3. **Monitor first few runs** to ensure everything works
4. **Keep messages natural** to avoid spam detection
5. **Respect Telegram limits** - don't spam

---

## 📞 Need Help?

1. Check [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed guide
2. Review workflow logs in Actions tab
3. Test locally with `python scheduled_group_sender.py`
4. Verify secrets are set correctly

---

**You're all set! 🎉**

The bot will now send messages to your groups automatically every hour!
