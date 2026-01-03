# 🌐 Deployment Guide - Making Your HRMS Live

## Step 1: Upload to GitHub

### 1.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `dayflow-hrms` (or your choice)
3. Description: "HRMS with Email OTP and Pre-Registration System"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

### 1.2 Upload Your Code

```bash
cd C:\Users\Lenovo\OneDrive\Desktop\hackthon\Dayflow-HRMS

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: DayFlow HRMS"

# Add your GitHub repo (replace USERNAME and REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Web (Make it Live)

### Option A: Render.com (RECOMMENDED - Free Tier)

#### 2.1 Prepare for Render

Create `render.yaml`:
```yaml
services:
  - type: web
    name: dayflow-hrms
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: MAIL_USERNAME
        sync: false
      - key: MAIL_PASSWORD
        sync: false
      - key: MAIL_DEFAULT_SENDER
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

Add `gunicorn` to requirements.txt:
```bash
echo gunicorn >> requirements.txt
```

Update `run.py` for production:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
```

#### 2.2 Deploy on Render

1. Go to https://render.com (sign up free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repo
5. Configure:
   - **Name**: dayflow-hrms
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
6. Add Environment Variables:
   - `MAIL_USERNAME` = your-email@gmail.com
   - `MAIL_PASSWORD` = your-app-password
   - `MAIL_DEFAULT_SENDER` = your-email@gmail.com
   - `SECRET_KEY` = (auto-generated or create your own)
7. Click "Create Web Service"
8. Wait 5-10 minutes for deployment
9. Your site will be live at: `https://dayflow-hrms.onrender.com`

---

### Option B: Railway.app (Easy, Free Tier)

1. Go to https://railway.app (sign up)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python
5. Add Environment Variables:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   SECRET_KEY=your-secret-key
   ```
6. Click "Deploy"
7. Go to Settings → Generate Domain
8. Your site: `https://dayflow-hrms.railway.app`

---

### Option C: PythonAnywhere (Easy Setup)

1. Go to https://www.pythonanywhere.com (free account)
2. Dashboard → "Web" → "Add a new web app"
3. Choose Flask framework
4. Upload your code:
   - Go to "Files" tab
   - Upload your project zip
   - Extract in `/home/yourusername/dayflow-hrms`
5. Configure WSGI file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):
   ```python
   import sys
   path = '/home/yourusername/dayflow-hrms'
   if path not in sys.path:
       sys.path.append(path)
   
   from run import app as application
   ```
6. Set environment variables:
   - Go to "Web" tab → Environment variables
   - Add MAIL_USERNAME, MAIL_PASSWORD, etc.
7. Reload web app
8. Visit: `https://yourusername.pythonanywhere.com`

---

### Option D: Heroku (Popular, Easy)

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create `Procfile` in project root:
   ```
   web: gunicorn run:app
   ```
3. Create `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create dayflow-hrms
   
   # Set environment variables
   heroku config:set MAIL_USERNAME=your-email@gmail.com
   heroku config:set MAIL_PASSWORD=your-app-password
   heroku config:set MAIL_DEFAULT_SENDER=your-email@gmail.com
   heroku config:set SECRET_KEY=your-secret-key
   
   git push heroku main
   ```
5. Your site: `https://dayflow-hrms.herokuapp.com`

---

## Step 3: Post-Deployment Setup

### 3.1 Create Admin on Live Site

**Method 1: Manually via Database**
- Connect to production database
- Run create_admin.py on server

**Method 2: Temporary Registration**
- Temporarily enable open registration
- Register admin account
- Disable open registration
- Update role to Admin in database

**Method 3: SSH/Console**
```bash
# On server console
python create_admin.py
```

### 3.2 Configure Production Settings

Update `config.py` for production:
```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Use PostgreSQL for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

---

## 📋 Pre-Deployment Checklist

- [ ] All sensitive data removed from code
- [ ] `.gitignore` configured correctly
- [ ] `requirements.txt` complete
- [ ] Email credentials ready
- [ ] Production WSGI server configured (gunicorn)
- [ ] Database migration strategy planned
- [ ] Backup strategy in place

---

## 🔒 Production Security

1. **Use PostgreSQL** instead of SQLite:
   ```bash
   pip install psycopg2-binary
   ```

2. **Enable HTTPS** (usually automatic on Render/Railway)

3. **Set strong SECRET_KEY**:
   ```python
   import secrets
   secrets.token_hex(32)
   ```

4. **Use environment variables** for all secrets

5. **Regular backups** of database

---

## 🐛 Common Issues

### Database not persisting
→ SQLite doesn't work well on some platforms
→ Use PostgreSQL (provided free by Render/Railway)

### Static files not loading
→ Configure static file serving in production
→ Use WhiteNoise middleware

### Email not working
→ Verify environment variables are set correctly
→ Check email provider allows SMTP from your host

### App crashes on startup
→ Check logs: `heroku logs --tail` or platform-specific logs
→ Verify all dependencies in requirements.txt

---

## 📊 Monitoring

- **Render**: Built-in logs and metrics
- **Railway**: Built-in observability
- **Heroku**: Use `heroku logs --tail`
- **PythonAnywhere**: Error logs in dashboard

---

## 💰 Cost Comparison

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| Render | 750 hrs/month | Best free option |
| Railway | $5 credit/month | Easy deployment |
| PythonAnywhere | 1 web app | Simple projects |
| Heroku | Limited hours | Established platform |

**Recommended: Render.com** (easiest + generous free tier)
