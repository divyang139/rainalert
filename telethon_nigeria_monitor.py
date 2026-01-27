import asyncio
import json
import logging
import os
import re
import time
from datetime import timedelta, timezone
from typing import Set, Tuple
from urllib.error import URLError
from urllib.request import urlopen

from telethon import TelegramClient, events
from telethon.errors import RPCError

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)

API_ID_ENV = "API_ID"
API_HASH_ENV = "API_HASH"
SOURCE_CHANNEL_ENV = "SOURCE_CHANNEL"
TARGET_CHANNEL_ENV = "TARGET_CHANNEL"

NIGERIA_TERMS = [
    "nigeria",
    "hausa",
    "urdu",
    "hindi",
   
]

def _term_to_pattern(term: str) -> re.Pattern:
    return re.compile(
        r"\b" + re.escape(term).replace("\\ ", r"\\s+") + r"\b",
        re.IGNORECASE,
    )

NIGERIA_PATTERN = re.compile(
    r"\b(?:" + "|".join(
        re.escape(term).replace("\\ ", r"\\s+") for term in NIGERIA_TERMS
    ) + r")\b",
    re.IGNORECASE,
)

KEYWORD_PATTERNS = [(term, _term_to_pattern(term)) for term in NIGERIA_TERMS]

KEYWORD_CONTEXT = {
    "nigeria": ("Nigeria", "🇳🇬", "Nigeria Users"),
    "hausa": ("Nigeria", "🇳🇬", "Nigeria Users"),
    "filipino": ("Philippines", "🇵🇭", "Philippines Users"),
    "hindi": ("India", "🇮🇳", "India Users"),
    "urdu": ("Pakistan", "🇵🇰", "Pakistan Users"),
}

DEFAULT_CONTEXT = ("Nigeria", "🇳🇬", "Nigeria Users")

CURRENCY_PATTERNS = [
    re.compile(r"(₦\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:per|/)\s*user)?)", re.IGNORECASE),
    re.compile(r"(NGN\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:per|/)\s*user)?)", re.IGNORECASE),
    re.compile(r"(Naira\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:per|/)\s*user)?)", re.IGNORECASE),
    re.compile(r"(\$\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:per|/)\s*user)?)", re.IGNORECASE),
    re.compile(r"(\d[\d,]*(?:\.\d+)?\s*(?:per\s+user))", re.IGNORECASE),
]

# Cache processed source message ids to prevent reposting duplicates during runtime.
processed_messages: Set[Tuple[int, int]] = set()


def get_env_value(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value.strip()


def sanitize_username(username: str) -> str:
    cleaned = username.lstrip("@")
    if not cleaned:
        raise ValueError("Channel username cannot be empty")
    return cleaned


def display_username(username: str) -> str:
    return f"@{username}" if not username.startswith("@") else username


def is_nigeria_alert(text: str) -> bool:
    return bool(NIGERIA_PATTERN.search(text))


def matched_keywords(text: str) -> Set[str]:
    detected: Set[str] = set()
    for term, pattern in KEYWORD_PATTERNS:
        if pattern.search(text):
            detected.add(term)
    return detected


def resolve_context(matched: Set[str]) -> Tuple[str, str, str]:
    for term in matched:
        context = KEYWORD_CONTEXT.get(term.lower())
        if context:
            return context
    return DEFAULT_CONTEXT


USD_INR_CACHE_TTL_SECONDS = 300
USD_INR_CACHE: dict = {"rate": None, "fetched_at": 0.0}


def get_usd_to_inr_rate() -> float:
    """Fetch live USD->INR rate with caching and fallback."""
    now = time.time()
    cached_rate = USD_INR_CACHE.get("rate")
    fetched_at = USD_INR_CACHE.get("fetched_at", 0.0)
    if cached_rate and (now - fetched_at) < USD_INR_CACHE_TTL_SECONDS:
        return cached_rate

    try:
        with urlopen("https://open.er-api.com/v6/latest/USD", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        rate = payload.get("rates", {}).get("INR")
        if isinstance(rate, (int, float)) and rate > 0:
            USD_INR_CACHE["rate"] = float(rate)
            USD_INR_CACHE["fetched_at"] = now
            return float(rate)
    except (URLError, ValueError, json.JSONDecodeError) as exc:
        logging.warning("Failed to fetch USD/INR rate, using fallback: %s", exc)

    return 91.0


def convert_usd_to_inr(amount_str: str, currency: str = "") -> str:
    """Convert USD amount to INR with live rate."""
    usd_match = re.search(r"\$\s?([\d,]+(?:\.\d+)?)", amount_str)
    if usd_match:
        usd_value = float(usd_match.group(1).replace(",", ""))
        rate = get_usd_to_inr_rate()
        inr_value = usd_value * rate
        currency_suffix = f" {currency}" if currency else ""
        return f"₹{inr_value:,.2f} (${usd_value:,.2f}){currency_suffix}"
    return amount_str


def extract_amount(text: str) -> str:
    for pattern in CURRENCY_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return "Not specified"


def extract_currency(text: str) -> str:
    """Extract currency code from source message like (XRP), (TRX), (USDT), etc."""
    currency_match = re.search(r"\(([A-Z]{3,10})\)", text)
    if currency_match:
        return currency_match.group(1)
    return "CRYPTO"


def clean_message(text: str) -> str:
    trimmed = text.strip()
    trimmed = re.sub(r"([\U00010000-\U0010FFFF])\1{2,}", r"\1\1", trimmed)
    trimmed = re.sub(r"\n{3,}", "\n\n", trimmed)
    trimmed = re.sub(r"[ \t]{2,}", " ", trimmed)
    cleaned_lines = []
    skip_block = False
    for line in trimmed.splitlines():
        normalized = line.lower().strip()
        if normalized.startswith("⭐️--- this week’s top rain collectors") or normalized.startswith("🌟--- this month’s top rain collectors"):
            skip_block = True
            continue
        if normalized.startswith("💸--- this week’s top rain givers") or normalized.startswith("🌾--- top 10 farmers"):
            skip_block = True
            continue
        if skip_block and (not normalized or normalized[0].isdigit() or normalized.startswith("1️⃣") or normalized.startswith("2️⃣") or normalized.startswith("3️⃣") or normalized.startswith("4️⃣") or normalized.startswith("5️⃣")):
            continue
        skip_block = False
        cleaned_lines.append(line)
    return "\n".join(line for line in cleaned_lines if line.strip())


def extract_detail_lines(text: str) -> Tuple[str, int, str]:
    by_line = None
    users_line = None
    user_count = 0
    users_list = []
    
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("🎁") or stripped.lower().startswith("by:"):
            # Extract just the "By: rain-bot" part
            by_text = stripped.replace("🎁", "").strip()
            if by_text.lower().startswith("by:"):
                by_line = f"🎯 {by_text}"
            else:
                by_line = f"🎯 By: {by_text}"
        elif stripped.startswith("👥"):
            # Extract users from "👥 Users: name1, name2, name3..."
            users_text = stripped[1:].strip()
            if ":" in users_text:
                label, users_part = users_text.split(":", 1)
                users_list = [u.strip() for u in users_part.split(",") if u.strip()]
                user_count = len(users_list)
                # Format users as clean bulleted list
                formatted_users = "\n".join([f"   • <b>{user}</b>" for user in users_list])
                users_line = f"👤 Users:\n{formatted_users}"
    
    # Return users first, then by
    result = []
    if users_line:
        result.append(users_line)
    if by_line:
        result.append(by_line)
    return "\n\n".join(result), user_count, ", ".join(users_list) if users_list else ""


def format_message(raw_text: str, source_display: str, msg_timestamp: str) -> str:
    cleaned_text = clean_message(raw_text)
    amount = extract_amount(raw_text)
    currency = extract_currency(raw_text)
    amount_with_inr = convert_usd_to_inr(amount, currency)
    keyword_hits = matched_keywords(raw_text)
    country, flag, _audience = resolve_context(keyword_hits)
    detail_block, user_count, users_str = extract_detail_lines(raw_text)
    
    # Clean user count line - only show if we have users
    user_count_line = f"👥 Total Users: {user_count}" if user_count > 0 else ""
    
    return (
        f"🌧 RAIN ALERT — {country.upper()} {flag}\n\n"
        f"💵 Amount per User: {amount_with_inr}\n"
        f"{user_count_line}\n\n"
        f"{detail_block}"
    )


def ensure_timestamp_string(dt) -> str:
    ist = timezone(timedelta(hours=5, minutes=30), name="IST")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(ist)
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")



def register_event_handler(client: TelegramClient, source_channel: str, target_channel: str, source_display: str) -> None:
    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        if not event.raw_text:
            return

        text = event.raw_text
        if not is_nigeria_alert(text):
            return

        message_key = (event.message.chat_id, event.message.id)
        if message_key in processed_messages:
            return

        processed_messages.add(message_key)
        
        # Limit cache size to prevent memory leaks
        if len(processed_messages) > 500:
            oldest_items = list(processed_messages)[:100]
            for item in oldest_items:
                processed_messages.discard(item)

        timestamp = ensure_timestamp_string(event.message.date)
        outbound_message = format_message(text, source_display, timestamp)
        
        # Detect country for logging
        keyword_hits = matched_keywords(text)
        country_name, _, _ = resolve_context(keyword_hits)

        try:
            # Add delay to reduce spam/ban risk
            await asyncio.sleep(1.5)
            await client.send_message(target_channel, outbound_message, parse_mode="html")
        except RPCError as exc:
            logging.error("Failed to forward alert id=%s: %s", event.message.id, exc)
            processed_messages.discard(message_key)
            return


def main() -> None:
    try:
        api_id = int(get_env_value(API_ID_ENV))
        api_hash = get_env_value(API_HASH_ENV)
        source_channel_raw = get_env_value(SOURCE_CHANNEL_ENV)
        target_channel_raw = get_env_value(TARGET_CHANNEL_ENV)
    except (RuntimeError, ValueError) as exc:
        logging.error(exc)
        raise SystemExit(1) from exc

    source_channel = sanitize_username(source_channel_raw)
    target_channel = sanitize_username(target_channel_raw)

    source_display = display_username(source_channel_raw)
    target_display = display_username(target_channel_raw)

    client = TelegramClient("nigeria_rain_monitor", api_id, api_hash)

    register_event_handler(client, source_channel, target_channel, source_display)

    async def runner():
        await client.start()
        await client.get_entity(source_channel)
        await client.get_entity(target_channel)
        await client.run_until_disconnected()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        pass
    finally:
        if not client.is_connected():
            client.disconnect()


if __name__ == "__main__":
    main()
