from telethon import TelegramClient
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
target_channel = os.getenv("TARGET_CHANNEL")

client = TelegramClient("nigeria_rain_monitor", api_id, api_hash)

async def main():
    await client.start()
    await client.send_message(
        target_channel,
        "✅ TEST MESSAGE\n\n🌧️ Rain Alert Bot is working correctly!"
    )
    print("Test message sent successfully!")

with client:
    client.loop.run_until_complete(main())
