"""
Test script to verify GitHub Actions environment variables
"""
import os
from telethon import TelegramClient

def test_environment():
    """
    Test if all required environment variables are set
    """
    print("🔍 Testing GitHub Actions Environment Variables...\n")
    
    required_vars = {
        'API_ID': os.getenv('API_ID'),
        'API_HASH': os.getenv('API_HASH'),
        'PHONE_NUMBER': os.getenv('PHONE_NUMBER'),
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            # Mask sensitive values
            masked_value = var_value[:4] + '*' * (len(var_value) - 4) if len(var_value) > 4 else '****'
            print(f"✅ {var_name}: {masked_value}")
        else:
            print(f"❌ {var_name}: NOT SET")
            all_set = False
    
    if all_set:
        print("\n✅ All environment variables are set!")
        print("\n🔄 Testing Telegram connection...")
        test_telegram_connection(required_vars)
    else:
        print("\n❌ Some environment variables are missing!")
        print("Make sure to set them in GitHub Secrets.")
        return False
    
    return True

def test_telegram_connection(env_vars):
    """
    Test connection to Telegram API
    """
    try:
        api_id = int(env_vars['API_ID'])
        api_hash = env_vars['API_HASH']
        phone = env_vars['PHONE_NUMBER']
        
        client = TelegramClient('test_session', api_id, api_hash)
        
        print("📞 Connecting to Telegram...")
        client.connect()
        
        if client.is_user_authorized():
            print("✅ Successfully connected to Telegram!")
            print(f"📱 Phone: {phone[:5]}*****{phone[-2:]}")
        else:
            print("⚠️ Connected but not authorized. Session file may be invalid.")
        
        client.disconnect()
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")

if __name__ == "__main__":
    test_environment()
