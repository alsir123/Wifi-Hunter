from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
import asyncio
import json
import os
import logging

logging.basicConfig(level=logging.WARNING)

api_id = int(os.environ["TG_API_ID"])
api_hash = os.environ["TG_API_HASH"]
phone = os.environ["TG_PHONE"]
password = os.environ.get("TG_PASSWORD")

SETTINGS_FILE = 'bot_settings.json'

default_settings = {
    'bot_active': True,
    'welcome_msg': 'انا مساعد دولة الشخصي، ترك رسالتك وساعاود الاتصال بك سيدي',
    'warning_msg': '⚠️ سيتم حظرك إن عاودت المحاولة!',
    'block_msg': '🚫 تم حظرك بسبب تكرار الرسائل.',
    'max_msgs': 2,
    'auto_block': True,
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default_settings.copy()

def save_settings(s):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

settings = load_settings()
message_count = {}
waiting_for = {}

client = TelegramClient('dawlah_v5', api_id, api_hash,
                        receive_updates=True,
                        retry_delay=5,
                        connection_retries=5,
                        auto_reconnect=True)

# === لوحة التحكم ===
@client.on(events.NewMessage(outgoing=True, pattern=r'^/panel$'))
async def panel(event):
    status = "🟢 شغال" if settings['bot_active'] else "🔴 متوقف"
    block = "🟢 مفعّل" if settings['auto_block'] else "🔴 معطّل"
    await event.reply(
        f"⚙️ **لوحة تحكم بوت دولة** ⚙️\n\n"
        f"حالة البوت: {status}\n"
        f"الحظر التلقائي: {block}\n\n"
        f"📋 **الأوامر:**\n"
        f"/on - تشغيل البوت\n"
        f"/off - إيقاف البوت\n"
        f"/msg - تعديل رسالة الترحيب\n"
        f"/warn - تعديل رسالة التحذير\n"
        f"/blockmsg - تعديل رسالة الحظر\n"
        f"/blockon - تفعيل الحظر التلقائي\n"
        f"/blockoff - تعطيل الحظر التلقائي\n"
        f"/stats - إحصائيات\n"
        f"/reset - إعادة تعيين العدادات\n"
        f"/show - عرض الإعدادات والرسائل\n"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r'^/on$'))
async def bot_on(event):
    settings['bot_active'] = True
    save_settings(settings)
    await event.reply("✅ تم تشغيل البوت")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/off$'))
async def bot_off(event):
    settings['bot_active'] = False
    save_settings(settings)
    await event.reply("🔴 تم إيقاف البوت")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/msg$'))
async def edit_msg(event):
    me = await client.get_me()
    waiting_for[me.id] = 'welcome_msg'
    await event.reply(f"✏️ الرسالة الحالية:\n{settings['welcome_msg']}\n\nأرسل الرسالة الجديدة الآن (أو /cancel للإلغاء):")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/warn$'))
async def edit_warn(event):
    me = await client.get_me()
    waiting_for[me.id] = 'warning_msg'
    await event.reply(f"✏️ رسالة التحذير الحالية:\n{settings['warning_msg']}\n\nأرسل الرسالة الجديدة (أو /cancel):")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/blockmsg$'))
async def edit_blockmsg(event):
    me = await client.get_me()
    waiting_for[me.id] = 'block_msg'
    await event.reply(f"✏️ رسالة الحظر الحالية:\n{settings['block_msg']}\n\nأرسل الرسالة الجديدة (أو /cancel):")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/blockon$'))
async def block_on(event):
    settings['auto_block'] = True
    save_settings(settings)
    await event.reply("🟢 تم تفعيل الحظر التلقائي")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/blockoff$'))
async def block_off(event):
    settings['auto_block'] = False
    save_settings(settings)
    await event.reply("🔴 تم تعطيل الحظر التلقائي")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/stats$'))
async def stats(event):
    total = len(message_count)
    total_msgs = sum(message_count.values())
    blocked = sum(1 for v in message_count.values() if v > settings['max_msgs'] + 1)
    status = "🟢 شغال" if settings['bot_active'] else "🔴 متوقف"
    await event.reply(
        f"📊 **إحصائيات** 📊\n\n"
        f"حالة البوت: {status}\n"
        f"👥 عدد المراسلين: {total}\n"
        f"💬 إجمالي الرسائل: {total_msgs}\n"
        f"🚫 تم حظرهم: {blocked}"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r'^/reset$'))
async def reset(event):
    message_count.clear()
    await event.reply("✅ تم إعادة تعيين جميع العدادات")

@client.on(events.NewMessage(outgoing=True, pattern=r'^/show$'))
async def show(event):
    status = "🟢 شغال" if settings['bot_active'] else "🔴 متوقف"
    block = "🟢 مفعّل" if settings['auto_block'] else "🔴 معطّل"
    await event.reply(
        f"📋 **الإعدادات الحالية** 📋\n\n"
        f"حالة البوت: {status}\n"
        f"الحظر التلقائي: {block}\n"
        f"عدد الرسائل قبل التحذير: {settings['max_msgs']}\n\n"
        f"💬 رسالة الترحيب:\n{settings['welcome_msg']}\n\n"
        f"⚠️ رسالة التحذير:\n{settings['warning_msg']}\n\n"
        f"🚫 رسالة الحظر:\n{settings['block_msg']}"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r'^/cancel$'))
async def cancel(event):
    me = await client.get_me()
    if me.id in waiting_for:
        del waiting_for[me.id]
    await event.reply("❌ تم الإلغاء")

# استقبال النص الجديد
@client.on(events.NewMessage(outgoing=True))
async def receive_text(event):
    if event.text.startswith('/'):
        return
    me = await client.get_me()
    if me.id not in waiting_for:
        return

    field = waiting_for[me.id]
    settings[field] = event.text
    save_settings(settings)
    del waiting_for[me.id]

    names = {'welcome_msg': 'رسالة الترحيب', 'warning_msg': 'رسالة التحذير', 'block_msg': 'رسالة الحظر'}
    await event.reply(f"✅ تم تحديث {names.get(field)}!\n\nالنص الجديد:\n{event.text}")

# === الرد التلقائي ===
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply(event):
    try:
        sender = await event.get_sender()
        me = await client.get_me()

        if sender.id == me.id:
            return
        if sender.bot:
            return
        if not settings['bot_active']:
            return

        sid = sender.id
        if sid not in message_count:
            message_count[sid] = 0
        message_count[sid] += 1

        if message_count[sid] <= settings['max_msgs']:
            await event.reply(settings['welcome_msg'])
        elif message_count[sid] == settings['max_msgs'] + 1:
            await event.reply(settings['warning_msg'])
        else:
            if settings['auto_block']:
                await event.reply(settings['block_msg'])
                await client(BlockRequest(id=sid))
                print(f"تم حظر: {sid}")
            else:
                await event.reply(settings['warning_msg'])
    except Exception as e:
        print(f"خطأ: {e}")

async def main():
    print("جاري تسجيل الدخول...")
    await client.start(phone=phone, password=password)
    me = await client.get_me()
    print(f"تم تسجيل الدخول: {me.first_name}")
    print("البوت شغال... اضغط Ctrl+C لايقافه")
    print("أرسل /panel في الرسائل المحفوظة لفتح لوحة التحكم")
    await client.catch_up()
    await client.run_until_disconnected()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nتم إيقاف البوت")
except Exception as e:
    print(f"خطأ: {e}")
