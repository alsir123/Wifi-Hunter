import os
import time

from telethon import TelegramClient, events

api_id_raw = os.environ.get("TELEGRAM_API_ID")
api_hash = os.environ.get("TELEGRAM_API_HASH")

if not api_id_raw or not api_hash:
    raise SystemExit(
        "Set TELEGRAM_API_ID and TELEGRAM_API_HASH (get them from "
        "https://my.telegram.org) before running."
    )

api_id = int(api_id_raw)
session_name = os.environ.get("TELEGRAM_SESSION", "userbot")

client = TelegramClient(session_name, api_id, api_hash)

# AFK state
afk = {"active": False, "reason": "", "since": 0.0}
# Users we've already auto-replied to during the current AFK period
replied = set()
# IDs of messages the userbot itself sent as auto-replies, so the outgoing
# handler doesn't mistake them for genuine user activity
own_replies = set()


def _afk_duration() -> str:
    seconds = int(time.time() - afk["since"])
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    return f"{hours}h {minutes % 60}m"


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.afk(?:\s+(.*))?$"))
async def set_afk(event):
    reason = (event.pattern_match.group(1) or "").strip()
    afk["active"] = True
    afk["reason"] = reason
    afk["since"] = time.time()
    replied.clear()
    msg = "I'm AFK now."
    if reason:
        msg += f" Reason: {reason}"
    await event.edit(msg)


@client.on(events.NewMessage(outgoing=True))
async def clear_afk_on_activity(event):
    if event.id in own_replies:
        own_replies.discard(event.id)
        return
    text = event.raw_text or ""
    if text.startswith(".afk"):
        return
    if afk["active"]:
        afk["active"] = False
        afk["reason"] = ""
        replied.clear()
        await event.respond("I'm back — AFK disabled.")


@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if not afk["active"]:
        return
    if not event.is_private:
        return
    sender = await event.get_sender()
    if sender is None or getattr(sender, "bot", False):
        return
    if event.sender_id in replied:
        return
    replied.add(event.sender_id)
    reply = f"I'm currently away (AFK for {_afk_duration()}). I'll reply as soon as I'm back."
    if afk["reason"]:
        reply += f"\nReason: {afk['reason']}"
    sent = await event.reply(reply)
    own_replies.add(sent.id)


def main() -> None:
    print("Userbot starting... (first run will ask for your phone number and code)")
    client.start()
    print("Userbot is running. Use .afk [reason] to enable auto-reply.")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
