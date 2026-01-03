# 🚀 Quick Setup Guide for GitHub Users

## ⚠️ IMPORTANT: First-Time Setup

After cloning this repository, follow these steps to get started:

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Email (REQUIRED for OTP)

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate new app password
3. Copy the 16-character password

**Set Environment Variables:**

**Windows PowerShell:**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password-here"
$env:MAIL_DEFAULT_SENDER="your-email@gmail.com"
```

**Linux/Mac:**
```bash
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-app-password-here"
export MAIL_DEFAULT_SENDER="your-email@gmail.com"
```

### 3. Create Admin Account

```bash
python create_admin.py
```

**Important:** Edit `create_admin.py` first to set your email and password!

### 4. Run Application

```bash
python run.py
```

Visit: **http://127.0.0.1:5000**

---

## 🔐 How Authentication Works

### 1. Pre-Registration (HR Only)
- HR logs in and goes to "Pre-Register Employees"
- Adds Employee ID + Email for each new employee
- This authorizes them to register

### 2. Employee Registration
- Employee goes to registration page
- Must use EXACT Employee ID from HR
- Must use EXACT Email from HR
- Creates password
- If ID/Email doesn't match → Registration blocked

### 3. Login with OTP
- Enter email + password
- OTP sent to email (6-digit code)
- Enter OTP within 10 minutes
- Logged in successfully

---

## 📝 Quick Start Steps

1. **Admin registers pre-approved employees**
   ```
   Admin Dashboard → Pre-Register Employees → Add employee details
   ```

2. **Employee registers using HR-provided credentials**
   ```
   Register page → Enter exact ID and email → Create password
   ```

3. **Login with OTP verification**
   ```
   Login → Email + Password → Check email → Enter OTP
   ```

---

## 🔧 Common Issues

### "Employee ID not found"
→ HR must pre-register you first

### "Email does not match"
→ Use the exact email HR registered

### "OTP not received"
→ Check spam folder
→ Verify email configuration
→ Wait 1 minute and try resend

### "Email credentials not configured"
→ Set MAIL_USERNAME and MAIL_PASSWORD environment variables

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

## 🛡️ Security Notes

- ✅ Passwords are hashed
- ✅ OTP expires in 10 minutes
- ✅ Email/ID validation prevents unauthorized access
- ✅ Session-based authentication
- ❌ Never commit `.env` or email credentials
- ❌ Never share your app password
