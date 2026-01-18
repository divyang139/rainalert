import asyncio
import logging
import os
from datetime import datetime
from typing import List

from telethon import TelegramClient, functions
from telethon.errors import RPCError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

API_ID_ENV = "API_ID"
API_HASH_ENV = "API_HASH"
TARGET_GROUPS_ENV = "TARGET_GROUPS"  # Comma-separated group usernames or IDs

# Default message template - customize as needed
DEFAULT_MESSAGE_TEMPLATE = """
🌟 Hourly Update 🌟

⏰ Time: {timestamp}

📢 Check out the latest rain alerts in our channel!
💰 Don't miss out on crypto rewards!

Stay active and keep chatting! 🚀
"""

# How often to send messages (in seconds)
SEND_INTERVAL = 3600  # 1 hour = 3600 seconds


def get_env_value(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value.strip()


def parse_target_groups(groups_str: str) -> List[str]:
    """Parse comma-separated group usernames/IDs/invite links"""
    groups = [g.strip() for g in groups_str.split(",") if g.strip()]
    if not groups:
        raise ValueError("No target groups specified")
    return groups


async def join_group_if_needed(client: TelegramClient, group_link: str):
    """Join group via invite link if not already a member"""
    try:
        # If it's an invite link, extract and join
        if "t.me/+" in group_link or "t.me/joinchat/" in group_link:
            # Extract hash from link
            hash_part = group_link.split("/")[-1]
            if hash_part.startswith("+"):
                hash_part = hash_part[1:]
            
            try:
                result = await client(functions.messages.ImportChatInviteRequest(hash_part))
                logging.info(f"✅ Joined group via invite link")
                return result.chats[0]
            except Exception as e:
                # Already joined or other error
                logging.debug(f"Note: {e}")
        
        # Try to get entity (works for already joined groups)
        return await client.get_entity(group_link)
    except Exception as exc:
        logging.error(f"Cannot access group {group_link}: {exc}")
        raise


def format_message(template: str) -> str:
    """Format message with current timestamp"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S IST")
    return template.format(timestamp=timestamp)


async def send_to_groups(client: TelegramClient, groups: List[str], message: str):
    """Send message to all target groups"""
    for group in groups:
        try:
            await client.send_message(group, message)
            logging.info(f"✅ Sent message to {group}")
            await asyncio.sleep(2)  # Small delay between sends
        except RPCError as exc:
            logging.error(f"❌ Failed to send to {group}: {exc}")


async def scheduled_sender(client: TelegramClient, groups: List[str]):
    """Main loop - send messages every hour"""
    logging.info(f"Starting scheduled sender for {len(groups)} groups")
    logging.info(f"Will send messages every {SEND_INTERVAL // 60} minutes")
    
    while True:
        try:
            message = format_message(DEFAULT_MESSAGE_TEMPLATE)
            logging.info("📤 Sending scheduled messages...")
            await send_to_groups(client, groups, message)
            logging.info(f"✅ Completed sending to all groups. Next send in {SEND_INTERVAL // 60} minutes.")
        except Exception as exc:
            logging.error(f"Error in scheduled sender: {exc}")
        
        await asyncio.sleep(SEND_INTERVAL)


async def main():
    try:
        api_id = int(get_env_value(API_ID_ENV))
        api_hash = get_env_value(API_HASH_ENV)
        groups_raw = get_env_value(TARGET_GROUPS_ENV)
    except (RuntimeError, ValueError) as exc:
        logging.error(exc)
        raise SystemExit(1) from exc

    target_groups = parse_target_groups(groups_raw)
    
    client = TelegramClient("scheduled_sender", api_id, api_hash)
    
    await client.start()
    logging.info("✅ Connected to Telegram")
    
    # Verify all groups exist and join if needed
    for group in target_groups:
        try:
            entity = await join_group_if_needed(client, group)
            logging.info(f"✅ Ready to send to group: {getattr(entity, 'title', group)}")
        except Exception as exc:
            logging.error(f"❌ Cannot access group {group}: {exc}")
    
    # Start scheduled sending
    try:
        await scheduled_sender(client, target_groups)
    except KeyboardInterrupt:
        logging.info("Shutdown requested by user")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
