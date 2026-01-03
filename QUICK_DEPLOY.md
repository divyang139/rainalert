# 🚀 Quick Deployment Steps

## ⚡ Fastest Way: Deploy to Render.com (5 minutes)

### 1. Upload to GitHub (2 minutes)

```bash
cd C:\Users\Lenovo\OneDrive\Desktop\hackthon\Dayflow-HRMS

git init
git add .
git commit -m "DayFlow HRMS - Ready for deployment"

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render (3 minutes)

1. Go to **https://render.com** → Sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** → Select your repository
4. Fill in:
   - **Name**: `dayflow-hrms`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
5. Click **"Advanced"** → Add Environment Variables:
   ```
   MAIL_USERNAME = your-email@gmail.com
   MAIL_PASSWORD = your-gmail-app-password
   MAIL_DEFAULT_SENDER = your-email@gmail.com
   SECRET_KEY = your-random-secret-key-here
   ```
6. Click **"Create Web Service"**
7. Wait 5-10 minutes ⏳
8. **Done!** Your site is live at: `https://dayflow-hrms.onrender.com` 🎉

### 3. Create Admin Account

After deployment, create admin via Render Shell:
1. Go to your service on Render
2. Click **"Shell"** tab
3. Run:
   ```bash
   python create_admin.py
   ```

---

## 📝 What's Already Done

✅ `Procfile` - Created (tells server how to run)
✅ `runtime.txt` - Created (specifies Python version)
✅ `requirements.txt` - Updated with gunicorn
✅ `config.py` - Credentials removed (uses environment variables)
✅ `.gitignore` - Configured to exclude sensitive files

---

## 🔑 Important Environment Variables

You need to set these on your hosting platform:

| Variable | Value |
|----------|-------|
| `MAIL_USERNAME` | your-email@gmail.com |
| `MAIL_PASSWORD` | your-gmail-app-password |
| `MAIL_DEFAULT_SENDER` | your-email@gmail.com |
| `SECRET_KEY` | (generate random: `python -c "import secrets; print(secrets.token_hex(32))"`) |

---

## 🌐 Alternative Hosting Options

### Railway.app
```bash
1. Go to railway.app
2. "New Project" → "Deploy from GitHub"
3. Select repo
4. Add environment variables
5. Done! (auto-detects Python)
```

### Heroku
```bash
heroku login
heroku create dayflow-hrms
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-gmail-app-password
heroku config:set MAIL_DEFAULT_SENDER=your-email@gmail.com
git push heroku main
```

---

## ✨ Your Website Will Be:

🌐 **Live URL**: `https://dayflow-hrms.onrender.com`
📧 **Email OTP**: Working automatically
🔐 **Secure**: HTTPS enabled by default
💾 **Database**: Auto-created SQLite (or upgrade to PostgreSQL)
🔄 **Auto-Deploy**: Updates when you push to GitHub

---

## 🎯 After Going Live

1. **Login as admin**: Use credentials from create_admin.py
2. **Pre-register employees**: Add their IDs and emails
3. **Share registration link**: Send to employees
4. **Monitor**: Check Render dashboard for logs and metrics

---

## ⚠️ Important Notes

- **Free Tier Limits**: 
  - Render: 750 hours/month (enough for 24/7)
  - May sleep after 15 min inactivity (wakes up automatically)
- **Custom Domain**: Can add your own domain later
- **Database**: SQLite works for small teams, upgrade to PostgreSQL for >50 users
- **Backups**: Download database regularly for safety

---

## 🆘 Need Help?

- Check logs on Render dashboard
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
- Common issues solved in deployment docs

**You're ready to deploy! 🚀**
