"""
Generate Telegram String Session for Telethon
Run this locally to get your STRING_SESSION
"""

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("=" * 50)
print("Telegram String Session Generator")
print("=" * 50)

# Get credentials from user
api_id = input("Enter API_ID: ").strip()
api_hash = input("Enter API_HASH: ").strip()

try:
    api_id = int(api_id)
except ValueError:
    print("❌ API_ID must be a number!")
    exit(1)

print("\n🔐 Starting authentication...")
print("You'll be asked to enter your phone number and verification code.\n")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print("\n" + "=" * 50)
    print("✅ SUCCESS! Your STRING_SESSION:")
    print("=" * 50)
    print(session_string)
    print("=" * 50)
    print("\n📋 Copy the above string and add it to your environment variables on TelebotHost:")
    print("   STRING_SESSION = <paste the string here>")
    print("\n⚠️  Keep this string SECRET - it gives full access to your account!")
