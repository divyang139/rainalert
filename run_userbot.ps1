# PowerShell Script to Run Telegram Userbot
# Loads environment variables and starts the userbot

Write-Host "🤖 Starting Telegram Userbot for Hourly Group Messages" -ForegroundColor Green
Write-Host ""

# Check if .env.userbot file exists
if (-Not (Test-Path ".env.userbot")) {
    Write-Host "❌ .env.userbot file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📝 Please follow these steps:" -ForegroundColor Yellow
    Write-Host "1. Copy .env.userbot.example to .env.userbot"
    Write-Host "2. Edit .env.userbot and add your credentials:"
    Write-Host "   - API_ID and API_HASH from https://my.telegram.org/apps"
    Write-Host "   - PHONE_NUMBER (with country code, e.g., +1234567890)"
    Write-Host "   - TARGET_GROUPS (comma-separated group usernames or links)"
    Write-Host ""
    exit 1
}

# Load environment variables from .env.userbot
Write-Host "📂 Loading environment variables..." -ForegroundColor Cyan
Get-Content .env.userbot | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        if ($name -and -not $name.StartsWith('#')) {
            [Environment]::SetEnvironmentVariable($name, $value, 'Process')
            Write-Host "   ✓ Loaded: $name" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "🚀 Starting userbot..." -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Run the userbot
python hourly_group_sender.py
