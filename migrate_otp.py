"""
Database migration script to add OTP table
Run this script to update your database schema with OTP support
"""

from app import create_app, db
from app.models import OTP

def migrate_database():
    """Create OTP table in existing database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create OTP table
            db.create_all()
            print("✓ Database migration successful!")
            print("✓ OTP table created")
            print("\nYou can now use email OTP authentication.")
            print("\nTo configure email settings, set these environment variables:")
            print("  - MAIL_SERVER (e.g., smtp.gmail.com)")
            print("  - MAIL_PORT (e.g., 587)")
            print("  - MAIL_USERNAME (your email)")
            print("  - MAIL_PASSWORD (your app password)")
            print("  - MAIL_DEFAULT_SENDER (sender email)")
            print("\nOr run without email configuration for development mode.")
            
        except Exception as e:
            print(f"✗ Migration failed: {str(e)}")
            print("\nIf the table already exists, you can safely ignore this error.")

if __name__ == '__main__':
    migrate_database()
