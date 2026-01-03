# Email OTP Authentication Setup Guide

## Overview
Email OTP (One-Time Password) authentication has been added to the DayFlow HRMS system. Users must now verify their identity using a 6-digit code sent to their email after entering their credentials.

## Features Added

### 1. OTP Model (`app/models.py`)
- New `OTP` table to store verification codes
- Fields: email, otp_code, purpose, is_used, expires_at
- OTP validation with expiry checking

### 2. Email Configuration (`config.py`)
- SMTP email settings
- OTP expiry time (default: 10 minutes)
- OTP length (default: 6 digits)

### 3. Email Utilities (`app/email_utils.py`)
- `send_email()` - Generic email sender with HTML/text support
- `send_otp_email()` - Specialized OTP email with styled template
- Development mode support (prints OTP to console if email not configured)

### 4. Authentication Routes (`app/routes/auth.py`)
- `generate_otp()` - Generates random 6-digit code
- `create_otp()` - Creates and stores OTP in database
- `verify_otp_code()` - Validates OTP code
- `/login` - Updated to send OTP after password verification
- `/verify-otp` - New route for OTP verification
- `/resend-otp` - Allows users to request new OTP

### 5. OTP Verification Page (`app/templates/auth/verify_otp.html`)
- Clean, user-friendly OTP input interface
- Auto-submit when 6 digits entered
- Paste support for OTP codes
- Resend OTP functionality
- Mobile-responsive design

## Configuration

### Email Settings (Environment Variables)

For production, set these environment variables:

```bash
# Email server settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@dayflow.com
```

### For Gmail:
1. Enable 2-Factor Authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password (not your regular password)

### For Other Email Providers:
- **Outlook/Office365**: `smtp.office365.com`, port 587
- **Yahoo**: `smtp.mail.yahoo.com`, port 587
- **SendGrid**: `smtp.sendgrid.net`, port 587

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update database schema:**
   ```bash
   # Using Python shell
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ```

   Or delete the existing database and recreate:
   ```bash
   # PowerShell
   Remove-Item instance\dayflow.db
   python run.py
   ```

3. **Configure email settings** (optional for development):
   Create a `.env` file or set environment variables as shown above.

## Development Mode

If email is not configured, the system will:
- Display OTP in flash messages on the page
- Print OTP to console/logs
- Still function normally for testing

## Authentication Flow

1. User enters email and password on login page
2. System validates credentials
3. If valid, generates 6-digit OTP
4. OTP is sent to user's email
5. User is redirected to OTP verification page
6. User enters OTP within 10 minutes
7. System validates OTP
8. User is logged in and redirected to dashboard

## Security Features

- **OTP Expiry**: Codes expire after 10 minutes
- **Single Use**: Each OTP can only be used once
- **Invalidation**: Old OTPs are invalidated when new ones are generated
- **Session-based**: Email stored in session for verification
- **Purpose-specific**: OTPs are tied to specific purposes (login, registration, etc.)

## Testing

### Without Email Configuration:
1. Login with valid credentials
2. OTP will be displayed in a flash message
3. Copy the OTP and paste in verification page
4. Click "Verify OTP"

### With Email Configuration:
1. Login with valid credentials
2. Check your email inbox for OTP
3. Enter the 6-digit code
4. Submit to complete login

## Future Enhancements

Potential additions:
- SMS OTP as alternative to email
- OTP rate limiting to prevent abuse
- Remember device feature to skip OTP
- Admin setting to enable/disable OTP
- OTP analytics and monitoring

## Troubleshooting

### OTP Not Received:
1. Check spam/junk folder
2. Verify email configuration
3. Check console logs for errors
4. Use "Resend OTP" button

### Invalid OTP Error:
1. Ensure OTP was copied correctly
2. Check if OTP has expired (10 minutes)
3. Request new OTP using "Resend OTP"

### Email Configuration Errors:
1. Verify SMTP settings
2. Check firewall/network restrictions
3. Ensure app password is correct (for Gmail)
4. Check email provider's SMTP documentation

## Database Schema

### OTP Table:
```sql
CREATE TABLE otp (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    purpose VARCHAR(20) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_otp_email ON otp(email);
```

## Files Modified/Created

### Modified:
- `app/models.py` - Added OTP model
- `config.py` - Added email and OTP settings
- `app/routes/auth.py` - Updated login flow with OTP
- `requirements.txt` - Added Flask-Mail

### Created:
- `app/email_utils.py` - Email sending utilities
- `app/templates/auth/verify_otp.html` - OTP verification page
- `OTP_SETUP.md` - This documentation

## Support

For issues or questions:
1. Check this documentation
2. Review console logs
3. Verify configuration settings
4. Test with development mode first
