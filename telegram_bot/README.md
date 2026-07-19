# Telegram Bot

A simple Telegram bot built with [python-telegram-bot](https://python-telegram-bot.org/)
that responds to commands.

## Commands

- `/start` — Greets the user.
- `/help` — Lists available commands.
- `/echo <text>` — Repeats the given text.
- Any plain text message is echoed back.

## Setup

1. Create a bot and get a token from [@BotFather](https://t.me/BotFather).
2. Install dependencies:

   ```bash
   cd telegram_bot
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set your bot token:

   ```bash
   export TELEGRAM_BOT_TOKEN="123456:ABC-your-token"
   ```

   (or copy `.env.example` to `.env` and `source` it)

4. Run the bot:

   ```bash
   python3 bot.py
   ```

The bot uses long polling, so no public URL or webhook setup is required.

## Userbot (auto-reply / AFK)

`userbot.py` runs on **your own Telegram account** (via [Telethon](https://docs.telethon.dev/))
and auto-replies to private messages while you're away.

### Commands (send from your own account)

- `.afk [reason]` — enable AFK; while active, each person who DMs you gets a
  single auto-reply. Optional reason is included in the reply.
- Sending any other message turns AFK off automatically.

### Setup

1. Get `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).
2. Install dependencies (`pip install -r requirements.txt`).
3. Set credentials:

   ```bash
   export TELEGRAM_API_ID="1234567"
   export TELEGRAM_API_HASH="your-api-hash"
   ```

4. Run and log in (first run asks for your phone number + code, and 2FA
   password if enabled):

   ```bash
   python3 userbot.py
   ```

The login is saved to a local `userbot.session` file, so you only log in once.
