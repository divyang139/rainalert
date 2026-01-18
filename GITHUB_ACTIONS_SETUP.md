# 🚀 Running Userbot on GitHub Actions

This guide will help you run your Telegram userbot scheduler on GitHub Actions, which runs automatically on GitHub's servers.

## ✅ Prerequisites

1. **GitHub Account** - Free account works fine
2. **Telegram API Credentials** - API ID and API Hash from https://my.telegram.org
3. **Session File** - Generated using `generate_session.py`

---

## 📋 Step-by-Step Setup

### Step 1: Generate Session File Locally

First, you need to generate the session file on your local machine:

```bash
# Install dependencies
pip install telethon

# Run the session generator
python generate_session.py
```

This will create `nigeria_rain_monitor.session` file.

### Step 2: Convert Session to Base64

You need to convert the session file to base64 format to store it as a GitHub Secret:

**On Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("nigeria_rain_monitor.session")) | Out-File session_base64.txt
```

**On Linux/Mac:**
```bash
base64 nigeria_rain_monitor.session > session_base64.txt
```

Copy the content of `session_base64.txt` - you'll need this for GitHub Secrets.

### Step 3: Push Code to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 4: Set Up GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `TELEGRAM_API_ID` | Your API ID | From my.telegram.org |
| `TELEGRAM_API_HASH` | Your API Hash | From my.telegram.org |
| `TELEGRAM_PHONE` | Your phone number | Format: +1234567890 |
| `SESSION_STRING` | Base64 session content | From step 2 |

### Step 5: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable workflows if prompted
3. You should see "Scheduled Userbot Messages" workflow

### Step 6: Test the Workflow

1. Go to **Actions** → **Scheduled Userbot Messages**
2. Click **Run workflow** → **Run workflow**
3. Wait for the workflow to complete
4. Check the logs to verify it worked

---

## ⚙️ Configuration

### Change Schedule

Edit `.github/workflows/scheduled_userbot.yml`:

```yaml
on:
  schedule:
    # Every hour
    - cron: '0 * * * *'
    
    # Every 30 minutes
    # - cron: '*/30 * * * *'
    
    # Every 2 hours
    # - cron: '0 */2 * * *'
    
    # Every day at 9 AM
    # - cron: '0 9 * * *'
```

### Modify Messages

Edit `scheduled_group_sender.py` to customize:
- Group chat IDs
- Messages to send
- Random message selection
- Time intervals

---

## 🔍 Monitoring

### View Logs

1. Go to **Actions** tab
2. Click on a workflow run
3. Click on the **send-messages** job
4. Expand steps to see detailed logs

### Check Last Run

The Actions tab shows:
- ✅ Successful runs (green checkmark)
- ❌ Failed runs (red X)
- Last run time
- Run duration

---

## ⚠️ Important Notes

### GitHub Actions Limits (Free Tier)

- **2,000 minutes/month** for private repositories
- **Unlimited** for public repositories
- Each run takes ~1-2 minutes
- Running hourly = ~720 minutes/month ✅

### Best Practices

1. **Keep session file secure** - Never commit to repository
2. **Use secrets** - Store all sensitive data in GitHub Secrets
3. **Monitor usage** - Check Actions usage in Settings → Billing
4. **Test locally first** - Always test changes locally before pushing

### Timezone

GitHub Actions runs in UTC timezone. If you need specific local times, adjust the cron schedule accordingly.

Example: To run at 9 AM EST (UTC-5):
```yaml
- cron: '0 14 * * *'  # 9 AM EST = 2 PM UTC (14:00)
```

---

## 🐛 Troubleshooting

### Workflow Not Running

- Check if Actions are enabled in repository settings
- Verify cron syntax is correct
- Make sure secrets are set correctly

### Session Errors

```
SessionPasswordNeededError
```
**Solution:** Disable 2FA temporarily or use app password

### Rate Limiting

```
FloodWaitError
```
**Solution:** Add delays between messages in the script

### Authentication Failed

```
ApiIdInvalidError
```
**Solution:** Verify API_ID and API_HASH secrets are correct

---

## 🔒 Security Considerations

1. **Private Repository** - Consider making your repo private
2. **Secrets Protection** - Never log or print secrets
3. **Session Security** - Session files have full account access
4. **Regular Updates** - Keep dependencies updated
5. **2FA Backup** - Keep backup codes safe

---

## 📊 Alternative: GitHub Actions with Schedule

For more complex scheduling, you can use multiple workflows:

**morning_messages.yml:**
```yaml
name: Morning Messages
on:
  schedule:
    - cron: '0 8 * * *'  # 8 AM daily
```

**evening_messages.yml:**
```yaml
name: Evening Messages
on:
  schedule:
    - cron: '0 20 * * *'  # 8 PM daily
```

---

## 🎯 Next Steps

1. ✅ Set up all GitHub Secrets
2. ✅ Test workflow manually
3. ✅ Monitor first few automatic runs
4. ✅ Customize messages and schedule
5. ✅ Set up notifications (optional)

---

## 📞 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Review Telegram API documentation
3. Verify all secrets are set correctly
4. Test locally first before deploying

**Happy Automating! 🎉**
