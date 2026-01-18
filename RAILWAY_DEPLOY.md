# Railway Deployment Guide

## 🚀 Deploy to Railway (Test at Your Own Risk)

⚠️ **Note**: Railway's ToS prohibits userbots. Use at your own risk.

### Step 1: Push to GitHub

```bash
cd C:\Users\Lenovo\OneDrive\Desktop\hackthon\Dayflow-HRMS

# Initialize git if not already
git init
git add telethon_nigeria_monitor.py Procfile requirements.txt
git commit -m "Add Telegram monitor"

# Create new GitHub repo and push
git remote add origin https://github.com/yourusername/telegram-monitor.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will auto-detect and deploy

### Step 3: Add Environment Variables

In Railway dashboard:
1. Click your project
2. Go to **Variables** tab
3. Add:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   SOURCE_CHANNEL=RainAnalytics
   TARGET_CHANNEL=yourchannelname
   TARGET_GROUPS=group1,group2,group3
   ```
4. Click **"Deploy"**

### Step 4: Handle Session File

⚠️ **Important**: Railway won't have your session file!

**Option A: Run locally first, then upload session**
```bash
# Run locally once to create session
python telethon_nigeria_monitor.py

# This creates: nigeria_rain_monitor.session

# Commit session to private repo (NEVER public!)
git add *.session
git commit -m "Add session"
git push
```

**Option B: Skip authentication** (advanced - modify script to accept phone/code via env vars)

### Step 5: Monitor Logs

Railway Dashboard → Your Project → **Deployments** → Click latest → **View Logs**

Watch for:
- ✅ "Listening for rain alerts..."
- ❌ Authentication errors
- ❌ Ban messages

## 📊 What to Watch For:

### Signs you might get flagged:
- Account gets banned from Railway (usually within hours/days)
- Project gets suspended
- Logs show "Terms violation"

### Tips to last longer:
1. Keep activity low (don't spam)
2. Don't advertise it's a userbot
3. Run only 1 instance
4. Monitor logs daily

## 🔄 If Railway Bans You:

**Fallback options:**
1. Move to DigitalOcean (with card)
2. Run on your PC
3. Try another platform (Render, etc.)

## 💡 Pro Tip:

Set up a **second Railway account** ahead of time (different email) as backup.

## ⏱️ Expected Runtime:

- **Optimistic**: Few weeks
- **Realistic**: Few days to 1 week
- **Worst case**: Hours

Good luck! 🤞
