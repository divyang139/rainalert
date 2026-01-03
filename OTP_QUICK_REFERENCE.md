# Quick Reference: Email OTP Authentication

## For Developers

### To Use in Development (No Email Setup Required):
```bash
python run.py
```
→ OTP will be displayed on screen when you log in

### To Use in Production (With Email):
1. Set environment variables:
   ```bash
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-app-password
   ```

2. Run application:
   ```bash
   python run.py
   ```

### Gmail App Password Setup:
1. Go to: https://myaccount.google.com/apppasswords
2. Generate new app password
3. Use that password (not your regular Gmail password)

## For Users

### Login Process:
1. Enter email and password
2. Click "Login"
3. Check your email for 6-digit code
4. Enter code on verification page
5. Click "Verify OTP"

### Didn't Receive OTP?
- Check spam/junk folder
- Click "Resend OTP" button
- Wait up to 1 minute for email delivery

### OTP Expired?
- Click "Resend OTP" to get a new code
- OTPs expire after 10 minutes

## File Locations

| Purpose | File |
|---------|------|
| OTP Routes | `app/routes/auth.py` |
| OTP Model | `app/models.py` |
| Email Config | `config.py` |
| Email Functions | `app/email_utils.py` |
| OTP Page | `app/templates/auth/verify_otp.html` |
| Config Example | `.env.example` |
| Documentation | `OTP_SETUP.md` |
| Test Script | `test_otp.py` |

## Key Functions

```python
# Generate OTP
from app.routes.auth import generate_otp
otp = generate_otp()  # Returns: "123456"

# Create and save OTP
from app.routes.auth import create_otp
otp = create_otp("user@example.com", "login")

# Verify OTP
from app.routes.auth import verify_otp_code
is_valid = verify_otp_code("user@example.com", "123456", "login")

# Send OTP email
from app.email_utils import send_otp_email
send_otp_email("user@example.com", "123456", "login")
```

## Configuration Values

| Setting | Default | Description |
|---------|---------|-------------|
| `OTP_EXPIRY_MINUTES` | 10 | How long OTP is valid |
| `OTP_LENGTH` | 6 | Number of digits in OTP |
| `MAIL_SERVER` | smtp.gmail.com | SMTP server address |
| `MAIL_PORT` | 587 | SMTP port |
| `MAIL_USE_TLS` | true | Use TLS encryption |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| OTP not received | Check email config, spam folder |
| "Invalid OTP" error | Check expiry, request new OTP |
| Email send fails | Verify SMTP settings, app password |
| Import errors | Run `pip install -r requirements.txt` |

## Testing Commands

```bash
# Test OTP functionality
python test_otp.py

# Run application
python run.py

# Update database
python migrate_otp.py
```

## Email Provider Settings

### Gmail:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

### Outlook:
```
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

### Yahoo:
```
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

## Security Notes

✓ OTPs expire after 10 minutes
✓ Each OTP can only be used once
✓ Old OTPs invalidated when new ones generated
✓ Email stored securely in session
✓ Development mode doesn't send real emails

## Need Help?

See `OTP_SETUP.md` for complete documentation
