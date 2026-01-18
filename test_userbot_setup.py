"""
Quick test script for Telegram userbot
Tests connection and group access without sending messages
"""

import asyncio
import os
from telethon import TelegramClient

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
TARGET_GROUPS = os.getenv("TARGET_GROUPS", "")


async def test_connection():
    """Test Telegram connection and group access"""
    
    print("🔍 Testing Telegram Userbot Setup\n")
    print("=" * 60)
    
    # Validate credentials
    if not API_ID or not API_HASH:
        print("❌ Missing API_ID or API_HASH")
        print("📝 Get these from https://my.telegram.org/apps")
        return False
    
    if not PHONE_NUMBER:
        print("❌ Missing PHONE_NUMBER")
        print("📝 Set your phone with country code (e.g., +1234567890)")
        return False
    
    if not TARGET_GROUPS:
        print("❌ Missing TARGET_GROUPS")
        print("📝 Add comma-separated group usernames or links")
        return False
    
    print("✅ Environment variables loaded")
    print(f"   API_ID: {API_ID}")
    print(f"   Phone: {PHONE_NUMBER}")
    
    # Parse groups
    groups = [g.strip() for g in TARGET_GROUPS.split(",") if g.strip()]
    print(f"   Groups: {len(groups)} configured\n")
    
    # Connect to Telegram
    print("🔌 Connecting to Telegram...")
    client = TelegramClient('userbot_session', int(API_ID), API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        
        me = await client.get_me()
        print(f"✅ Connected as: {me.first_name}")
        print(f"   Username: @{me.username}")
        print(f"   Phone: {me.phone}\n")
        
        # Test group access
        print("=" * 60)
        print("📋 Testing Group Access:\n")
        
        accessible = 0
        for i, group in enumerate(groups, 1):
            try:
                entity = await client.get_entity(group)
                title = getattr(entity, 'title', group)
                member_count = getattr(entity, 'participants_count', 'N/A')
                
                print(f"✅ {i}. {title}")
                print(f"   ID: {group}")
                print(f"   Members: {member_count}\n")
                
                accessible += 1
                
            except Exception as e:
                print(f"❌ {i}. {group}")
                print(f"   Error: {e}\n")
        
        print("=" * 60)
        print(f"\n📊 Summary: {accessible}/{len(groups)} groups accessible")
        
        if accessible == len(groups):
            print("\n✅ All groups accessible! You're ready to start the userbot.")
            print("\n🚀 Run: .\\run_userbot.ps1")
        elif accessible > 0:
            print(f"\n⚠️  Some groups are not accessible ({len(groups) - accessible} failed)")
            print("   Check group usernames/links and your membership")
        else:
            print("\n❌ No groups accessible. Please check your configuration.")
        
        return accessible > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        await client.disconnect()
        print("\n🔌 Disconnected")


if __name__ == "__main__":
    asyncio.run(test_connection())
