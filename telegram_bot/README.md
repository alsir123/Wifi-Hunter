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
