"""Email utility functions for sending emails"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def send_email(to_email, subject, html_body, text_body=None):
    """
    Send email using SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML content of the email
        text_body: Plain text content (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get email configuration
        mail_server = current_app.config['MAIL_SERVER']
        mail_port = current_app.config['MAIL_PORT']
        mail_username = current_app.config['MAIL_USERNAME']
        mail_password = current_app.config['MAIL_PASSWORD']
        mail_sender = current_app.config['MAIL_DEFAULT_SENDER']
        mail_use_tls = current_app.config['MAIL_USE_TLS']
        
        # Check if email is configured
        if not mail_username or not mail_password:
            logger.warning("Email not configured. Skipping email send.")
            # For development, print OTP to console
            if 'OTP' in subject or 'verification' in subject.lower():
                logger.info(f"OTP Email to {to_email}: {html_body}")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = mail_sender
        msg['To'] = to_email
        
        # Attach text and HTML parts
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)
        
        # Connect to SMTP server and send email
        print(f"[EMAIL] Attempting to send email to {to_email}")
        print(f"[EMAIL] SMTP: {mail_server}:{mail_port}, TLS: {mail_use_tls}")
        
        with smtplib.SMTP(mail_server, mail_port, timeout=30) as server:
            server.set_debuglevel(1)  # Enable debug output
            if mail_use_tls:
                print("[EMAIL] Starting TLS...")
                server.starttls()
            print("[EMAIL] Logging in...")
            server.login(mail_username, mail_password)
            print("[EMAIL] Sending message...")
            server.send_message(msg)
        
        print(f"[EMAIL] ✓ Email sent successfully to {to_email}")
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL] ✗ Failed to send email to {to_email}: {str(e)}")
        print(f"[EMAIL] Error type: {type(e).__name__}")
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def send_otp_email(to_email, otp_code, purpose='login'):
    """
    Send OTP verification email
    
    Args:
        to_email: Recipient email address
        otp_code: OTP code to send
        purpose: Purpose of OTP (login, registration, reset_password)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    purpose_text = {
        'login': 'Login Verification',
        'registration': 'Registration Verification',
        'reset_password': 'Password Reset'
    }.get(purpose, 'Verification')
    
    subject = f'DayFlow HRMS - {purpose_text} OTP'
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .content {{
                background-color: white;
                padding: 30px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                color: #4CAF50;
                text-align: center;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 5px;
                letter-spacing: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <h2>DayFlow HRMS - {purpose_text}</h2>
                <p>Hello,</p>
                <p>Your One-Time Password (OTP) for {purpose_text.lower()} is:</p>
                <div class="otp-code">{otp_code}</div>
                <p>This OTP is valid for {current_app.config['OTP_EXPIRY_MINUTES']} minutes.</p>
                <p><strong>Do not share this OTP with anyone.</strong></p>
                <p>If you did not request this OTP, please ignore this email.</p>
                <div class="footer">
                    <p>This is an automated email. Please do not reply.</p>
                    <p>&copy; 2026 DayFlow HRMS. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    DayFlow HRMS - {purpose_text}
    
    Hello,
    
    Your One-Time Password (OTP) for {purpose_text.lower()} is: {otp_code}
    
    This OTP is valid for {current_app.config['OTP_EXPIRY_MINUTES']} minutes.
    
    Do not share this OTP with anyone.
    
    If you did not request this OTP, please ignore this email.
    
    This is an automated email. Please do not reply.
    """
    
    return send_email(to_email, subject, html_body, text_body)
