@echo off
:: Batch Script to Run Telegram Userbot
:: Alternative to PowerShell script

echo.
echo ===================================================
echo    Telegram Hourly Group Message Userbot
echo ===================================================
echo.

:: Check if .env.userbot exists
if not exist ".env.userbot" (
    echo [ERROR] .env.userbot file not found!
    echo.
    echo Please follow these steps:
    echo 1. Copy .env.userbot.example to .env.userbot
    echo 2. Edit .env.userbot with your credentials
    echo 3. Get API credentials from https://my.telegram.org/apps
    echo.
    pause
    exit /b 1
)

:: Load environment variables
echo Loading configuration...
for /f "usebackq tokens=1,* delims==" %%A in (".env.userbot") do (
    if not "%%A"=="" (
        set %%A=%%B
        echo   - Loaded %%A
    )
)

echo.
echo Starting userbot...
echo Press Ctrl+C to stop
echo.

:: Run the Python script
python hourly_group_sender.py

if errorlevel 1 (
    echo.
    echo [ERROR] Userbot stopped with an error
    pause
)
