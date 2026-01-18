"""
Telegram Userbot for Hourly Group Messaging
Sends scheduled messages to 7-8 groups every hour
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import List, Dict
import random

from telethon import TelegramClient, functions
from telethon.errors import RPCError, FloodWaitError
from telethon.tl.types import Channel, Chat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("userbot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
TARGET_GROUPS = os.getenv("TARGET_GROUPS", "")  # Comma-separated

# Timing configuration
SEND_INTERVAL = 3600  # 1 hour in seconds
DELAY_BETWEEN_GROUPS = 5  # Delay between each group message (seconds)

# Multiple message templates to rotate
MESSAGE_TEMPLATES = [
    """
🌟 Hourly Update 🌟

⏰ Current Time: {timestamp}

📢 Stay active and engaged!
💬 Keep the conversation going!

🚀 Next update in 1 hour!
""",
    """
⚡ Quick Check-In ⚡

🕐 Time: {timestamp}

👋 Hello everyone!
💡 Hope you're having a great day!

See you in the next hour! 🎯
""",
    """
📣 Scheduled Reminder 📣

⏰ {timestamp}

✨ Don't forget to stay connected
🌐 Check out the latest updates

Back in an hour! ⏳
""",
    """
🎯 Hourly Broadcast 🎯

🕒 {timestamp}

💬 Keep chatting and stay engaged
🔥 Your activity matters!

Next update coming soon! 🚀
""",
    """
🌈 Regular Update 🌈

⏰ Time Check: {timestamp}

📱 Stay tuned for more updates
💪 Together we grow stronger!

See you in 60 minutes! ⌛
"""
]

# Custom messages for specific groups (optional)
CUSTOM_GROUP_MESSAGES = {
    # Example: "group_username": "Custom message for this group at {timestamp}"
}


class HourlyGroupSender:
    """Manages hourly message sending to multiple groups"""
    
    def __init__(self, api_id: str, api_hash: str, phone: str):
        self.api_id = int(api_id)
        self.api_hash = api_hash
        self.phone = phone
        self.client = None
        self.target_groups = []
        self.message_index = 0
        
    async def initialize(self):
        """Initialize Telegram client and verify connection"""
        try:
            self.client = TelegramClient('userbot_session', self.api_id, self.api_hash)
            await self.client.start(phone=self.phone)
            
            me = await self.client.get_me()
            logger.info(f"✅ Connected as: {me.first_name} (@{me.username})")
            logger.info(f"📱 Phone: {me.phone}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize client: {e}")
            return False
    
    def load_target_groups(self):
        """Load and validate target groups"""
        groups_str = TARGET_GROUPS
        if not groups_str:
            logger.error("❌ No target groups specified in TARGET_GROUPS environment variable")
            return False
        
        self.target_groups = [g.strip() for g in groups_str.split(",") if g.strip()]
        
        if not self.target_groups:
            logger.error("❌ No valid groups found")
            return False
        
        logger.info(f"📋 Loaded {len(self.target_groups)} target groups:")
        for i, group in enumerate(self.target_groups, 1):
            logger.info(f"   {i}. {group}")
        
        return True
    
    async def verify_groups(self):
        """Verify access to all groups and join if needed"""
        verified_groups = []
        
        for group_identifier in self.target_groups:
            try:
                # Check if it's an invite link
                if "t.me/+" in group_identifier or "t.me/joinchat/" in group_identifier:
                    entity = await self.join_via_invite_link(group_identifier)
                else:
                    # Try to get entity by username or ID
                    entity = await self.client.get_entity(group_identifier)
                
                if entity:
                    group_name = getattr(entity, 'title', group_identifier)
                    logger.info(f"✅ Verified access to: {group_name}")
                    verified_groups.append((group_identifier, entity))
                    
            except Exception as e:
                logger.error(f"❌ Cannot access group '{group_identifier}': {e}")
        
        if not verified_groups:
            logger.error("❌ No groups accessible. Cannot proceed.")
            return False
        
        self.target_groups = verified_groups
        logger.info(f"✅ Successfully verified {len(self.target_groups)} groups")
        return True
    
    async def join_via_invite_link(self, invite_link: str):
        """Join a group via invite link"""
        try:
            hash_part = invite_link.split("/")[-1]
            if hash_part.startswith("+"):
                hash_part = hash_part[1:]
            
            result = await self.client(functions.messages.ImportChatInviteRequest(hash_part))
            logger.info(f"✅ Joined group via invite link")
            return result.chats[0] if result.chats else None
            
        except FloodWaitError as e:
            logger.warning(f"⏰ Flood wait: Need to wait {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            return await self.join_via_invite_link(invite_link)
        except Exception as e:
            logger.debug(f"Note joining link: {e}")
            # Might already be member, try to get entity
            try:
                return await self.client.get_entity(invite_link)
            except:
                raise
    
    def format_message(self, template: str) -> str:
        """Format message with current timestamp"""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        return template.format(timestamp=timestamp)
    
    def get_next_message(self, group_identifier: str) -> str:
        """Get next message template (rotates through templates)"""
        # Check if there's a custom message for this group
        if group_identifier in CUSTOM_GROUP_MESSAGES:
            return self.format_message(CUSTOM_GROUP_MESSAGES[group_identifier])
        
        # Use rotating templates
        template = MESSAGE_TEMPLATES[self.message_index % len(MESSAGE_TEMPLATES)]
        return self.format_message(template)
    
    async def send_message_to_group(self, group_identifier, entity):
        """Send message to a single group with error handling"""
        try:
            message = self.get_next_message(group_identifier)
            await self.client.send_message(entity, message)
            
            group_name = getattr(entity, 'title', group_identifier)
            logger.info(f"✅ Sent to: {group_name}")
            return True
            
        except FloodWaitError as e:
            logger.warning(f"⏰ Flood wait for {group_identifier}: {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            # Retry after wait
            return await self.send_message_to_group(group_identifier, entity)
            
        except RPCError as e:
            logger.error(f"❌ RPC Error sending to {group_identifier}: {e}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error sending to {group_identifier}: {e}")
            return False
    
    async def send_to_all_groups(self):
        """Send messages to all groups with delays"""
        logger.info("=" * 60)
        logger.info("📤 Starting message broadcast to all groups...")
        
        successful = 0
        failed = 0
        
        for i, (group_identifier, entity) in enumerate(self.target_groups, 1):
            logger.info(f"📨 Sending to group {i}/{len(self.target_groups)}...")
            
            success = await self.send_message_to_group(group_identifier, entity)
            
            if success:
                successful += 1
            else:
                failed += 1
            
            # Add delay between messages to avoid flood
            if i < len(self.target_groups):
                logger.info(f"⏳ Waiting {DELAY_BETWEEN_GROUPS} seconds before next send...")
                await asyncio.sleep(DELAY_BETWEEN_GROUPS)
        
        # Rotate to next message template
        self.message_index += 1
        
        logger.info("=" * 60)
        logger.info(f"✅ Broadcast complete: {successful} successful, {failed} failed")
        logger.info(f"⏰ Next broadcast in {SEND_INTERVAL // 60} minutes")
        logger.info("=" * 60)
    
    async def run_scheduler(self):
        """Main scheduler loop - sends messages every hour"""
        logger.info("🚀 Starting hourly scheduler...")
        logger.info(f"⏱️  Interval: Every {SEND_INTERVAL // 60} minutes")
        logger.info(f"📊 Target Groups: {len(self.target_groups)}")
        
        cycle = 0
        
        while True:
            try:
                cycle += 1
                logger.info(f"\n🔄 Cycle #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                await self.send_to_all_groups()
                
                logger.info(f"\n💤 Sleeping for {SEND_INTERVAL // 60} minutes...\n")
                await asyncio.sleep(SEND_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("\n⏹️  Shutdown requested by user")
                break
                
            except Exception as e:
                logger.error(f"❌ Error in scheduler cycle: {e}")
                logger.info(f"⏳ Waiting 60 seconds before retry...")
                await asyncio.sleep(60)
    
    async def start(self):
        """Start the userbot"""
        try:
            logger.info("🤖 Initializing Hourly Group Sender Userbot...")
            
            # Initialize client
            if not await self.initialize():
                return False
            
            # Load target groups
            if not self.load_target_groups():
                return False
            
            # Verify group access
            if not await self.verify_groups():
                return False
            
            logger.info("\n✅ Setup complete! Starting scheduler...\n")
            
            # Run the scheduler
            await self.run_scheduler()
            
        except KeyboardInterrupt:
            logger.info("\n👋 Userbot stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
        finally:
            if self.client:
                await self.client.disconnect()
                logger.info("🔌 Disconnected from Telegram")


async def main():
    """Entry point"""
    # Validate environment variables
    if not API_ID or not API_HASH:
        logger.error("❌ Missing API_ID or API_HASH environment variables")
        logger.info("📝 Get these from https://my.telegram.org/apps")
        return
    
    if not PHONE_NUMBER:
        logger.error("❌ Missing PHONE_NUMBER environment variable")
        logger.info("📝 Set your phone number with country code (e.g., +1234567890)")
        return
    
    if not TARGET_GROUPS:
        logger.error("❌ Missing TARGET_GROUPS environment variable")
        logger.info("📝 Set comma-separated group usernames or invite links")
        return
    
    # Create and start userbot
    bot = HourlyGroupSender(API_ID, API_HASH, PHONE_NUMBER)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
