# Set your credentials here
$env:API_ID = "YOUR_API_ID_HERE"
$env:API_HASH = "YOUR_API_HASH_HERE"
$env:SOURCE_CHANNEL = "rainbot"
$env:TARGET_CHANNEL = "YOUR_TARGET_CHANNEL_HERE"

# Run the bot
Write-Host "Starting Nigeria Rain Monitor..." -ForegroundColor Green
py telethon_nigeria_monitor.py
