import os
import json
import datetime
import sqlite3
from http.server import BaseHTTPRequestHandler
import telebot
from telebot import types

# ==========================================
# ⚙ M.K HACKER SETTINGS & BOT CREDENTIALS:
# ==========================================
TOKEN = os.environ.get(
    "BOT_TOKEN", "9062431598:AAFuuI5MoCBRWIApQfWpdQvUVZ2yE8ZUWdY"
)
bot = telebot.TeleBot(TOKEN, threaded=False)

CHANNEL_ID = "-1004404606781"            # Force Subscribe Channel ID
LOG_CHANNEL_ID = -1004320753506         # Data Log Channel ID
BROADCAST_CHANNEL_ID = -1004322168174   # Broadcast Channel ID

CHANNEL_INVITE_LINK = "https://t.me/MK_HACKERR586"
OWNER_CONTACT = "https://t.me/MK_TRADER586"
BRAND_NAME = "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈"
BOT_NAME = "𓆩🪄𓆪 𝐌.𝐊 𝐀𝐈 𝐏𝐇𝐎𝐓𝐎 ENHANCER 𝐏𝐑𝐎 𓆩💫𓆪"
BOT_USERNAME = "@MK_AI_PHOTO_ENHANCER_BOT"
# ==========================================

# ==========================================
# 🗄️ SQLITE DATABASE SETUP (Permanent Storage)
# ==========================================
DB_FILE = "/tmp/hacker_ai_bot_database.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                joined_date TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS counters (
                key TEXT PRIMARY KEY,
                value INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Init error: {e}")

def get_next_request_count():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM counters WHERE key='request_count'")
        row = cursor.fetchone()
        count = (row[0] + 1) if row else 1
        cursor.execute("INSERT OR REPLACE INTO counters (key, value) VALUES ('request_count', ?)", (count,))
        conn.commit()
        conn.close()
        return count
    except Exception as e:
        print(f"Counter error: {e}")
        return 1

def save_user_to_db(user_id, username, full_name):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        pkt_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).strftime("%d %b %Y, %I:%M %p")
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, full_name, joined_date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, full_name, pkt_time))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"User save error: {e}")

def get_all_users():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Get users error: {e}")
        return []

init_db()

# Set Bot Commands (Left-side Menu Button Setup)
def set_bot_commands():
    try:
        commands = [
            types.BotCommand("start", "🚀 𝐒𝐓𝐀𝐑𝐓 𝐀𝐈 𝐄𝐍𝐇𝐀𝐍𝐂𝐄𝐑"),
            types.BotCommand("channel", "📢 𝐉𝐎𝐈𝐍 𝐌.𝐊 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋"),
            types.BotCommand("contact", "💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌.𝐊 𝐎𝐖𝐍𝐄𝐑 👑")
        ]
        bot.set_my_commands(commands)
    except Exception as e:
        print(f"Set commands error: {e}")

set_bot_commands()

# ==========================================
# 📊 M.K HACKER DATA LOG SYSTEM
# ==========================================
def send_data_to_log_channel(message, source_action):
    try:
        user = message.from_user
        if not user:
            return

        user_id = user.id
        username = f"@{user.username}" if user.username else "𝐍𝐨 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞"
        first_name = user.first_name or "N/A"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        save_user_to_db(user_id, username, full_name)
        
        chat_type = "𝑷𝒓𝒊𝒗𝒂𝒕𝒆 𝑪𝒉𝒂𝒕"
        if message.chat:
            if message.chat.type in ['group', 'supergroup']:
                chat_type = f"𝑮𝒓𝒐𝒖𝒑: {message.chat.title}"
            elif message.chat.type == 'channel':
                chat_type = f"𝑪𝒉𝒂𝒏𝒏𝒆𝒍: {message.chat.title}"
        
        req_number = get_next_request_count() if "Command" in source_action else "𝑵/𝑨"
        pkt_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        current_time = pkt_time.strftime("%d %b %Y, %I:%M %p")
        
        log_msg = (
            f"🔥☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 — 𝐃𝐀𝐓𝐀 𝐋𝐎𝐆 𝐒𝐘𝐒𝐓𝐄𝐌 ☠️🔥\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 𝐁𝐨𝐭 𝐍𝐚𝐦𝐞: {BOT_NAME}\n"
            f"👑 𝐁𝐫𝐚𝐧𝐝: {BRAND_NAME}\n"
            f"🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
            f"👤 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: {username}\n"
            f"📛 𝐍𝐚𝐦𝐞: {full_name}\n"
            f"💬 𝐈𝐧𝐭𝐞𝐫𝐚𝐜𝐭𝐢𝐨𝐧: {chat_type}\n"
            f"📊 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐂𝐨𝐮𝐧𝐭: #{req_number}\n"
            f"🛡️ 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐒𝐭𝐚𝐭𝐮𝐬: Secured & Verified ✅\n"
            f"🕐 𝐓𝐢𝐦𝐞: {current_time}\n"
            f"📱 𝐀𝐜𝐭𝐢𝐨𝐧 𝐒𝐨𝐮𝐫𝐜𝐞: {source_action}\n"
            f"🔥 𝐁𝐨𝐭: {BOT_USERNAME} 𓆩☠𓆪\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        sent_success = False
        try:
            photos = bot.get_user_profile_photos(user_id=user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                bot.send_photo(chat_id=LOG_CHANNEL_ID, photo=file_id, caption=log_msg)
                sent_success = True
        except Exception as inner_e:
            print(f"Photo error: {inner_e}")

        if not sent_success:
            bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_msg + "\n\n⚠️ 𝐔𝐒𝐄𝐑 𝐇𝐀𝐒 𝐍𝐎 𝐏𝐑𝐎𝐅𝐈𝐋𝐄 𝐏𝐇𝐎𝐓𝐎 ☠️")
    except Exception as e:
        print(f"Log error: {e}")

def verify_user_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["member", "creator", "administrator", "restricted"]:
            return True
    except Exception as e:
        print(f"Subscription check error: {e}")
    return False

# ==========================================
# 🤖 BOT HANDLERS (/start, /channel, /contact & Photos)
# ==========================================
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name if message.from_user.first_name else "User"

    if not verify_user_membership(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_join = types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url=CHANNEL_INVITE_LINK)
        btn_check = types.InlineKeyboardButton("✅ 𝐉𝐎𝐈𝐍𝐄𝐃 / 𝐂𝐎𝐍𝐅𝐈𝐑𝐌", callback_data="check_join")
        btn_contact = types.InlineKeyboardButton("💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈 𝐎𝐖𝐍𝐄𝐑", url=OWNER_CONTACT)
        markup.add(btn_join, btn_check, btn_contact)

        bot.send_message(
            message.chat.id,
            f"👋 𝐇𝐞𝐥𝐥𝐨 {user_name}!\n\n"
            f"🚨 𝐒𝐘𝐒𝐓𝐄𝐌 𝐀𝐂𝐂𝐄𝐒𝐒 𝐑𝐄𝐒𝐓𝐑𝐈𝐂𝐓𝐄𝐃\n\n"
            f"🔐 𝐉𝐨𝐢𝐧 𝐨𝐮𝐫 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐭𝐨 𝐮𝐧𝐥𝐨𝐜𝐤 𝐛𝐨𝐭 𝐚𝐜𝐜𝐞𝐬𝐬.\n\n"
            f"📌 𝐀𝐟𝐭𝐞𝐫 𝐣𝐨𝐢𝐧𝐢𝐧𝐠, 𝐜𝐥𝐢𝐜𝐤:\n"
            f"✅ 𝐉𝐎𝐈𝐍𝐄𝐃 / 𝐂𝐎𝐍𝐅𝐈𝐑𝐌",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        return

    send_data_to_log_channel(message, "Bot /start Command")
    show_main_menu(message.chat.id, user_name)

@bot.message_handler(commands=["channel"])
def channel_command(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url=CHANNEL_INVITE_LINK)
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "📢 **𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋**\n\n"
        "✨ **𝐒𝐭𝐚𝐲 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 • 𝐒𝐭𝐚𝐲 𝐔𝐩𝐝𝐚𝐭𝐞𝐝**\n\n"
        "🔥 𝐆𝐞𝐭 𝐭𝐡𝐞 𝐋𝐚𝐭𝐞𝐬𝐭 𝐔𝐩𝐝𝐚𝐭𝐞𝐬, 𝐍𝐞𝐰 𝐁𝐨𝐭 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬, "
        "𝐀𝐧𝐧𝐨𝐮𝐧𝐜𝐞𝐦𝐞𝐧𝐭𝐬, 𝐚𝐧𝐝 𝐄𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐑𝐞𝐥𝐞𝐚𝐬𝐞𝐬 "
        "𝐟𝐫𝐨𝐦 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑.\n\n"
        "👇 **𝐓𝐚𝐩 𝐭𝐡𝐞 𝐁𝐮𝐭𝐭𝐨𝐧 𝐁𝐞𝐥𝐨𝐰 𝐭𝐨 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥!**",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["contact"])
def contact_command(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈 𝐎𝐖𝐍𝐄𝐑", url=OWNER_CONTACT)
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "💬 **𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐎𝐖𝐍𝐄𝐑 👑**\n\n"
        "⚡ **𝐍𝐞𝐞𝐝 𝐇𝐞𝐥𝐩, 𝐂𝐮𝐬𝐭𝐨𝐦 𝐁𝐨𝐭𝐬, 𝐨𝐫 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐒𝐮𝐩𝐩𝐨𝐫𝐭?**\n\n"
        "🤖 𝐆𝐞𝐭 𝐇𝐞𝐥𝐩 𝐖𝐢𝐭𝐡 𝐁𝐨𝐭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭, "
        "𝐂𝐮𝐬𝐭𝐨𝐦 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬, 𝐚𝐧𝐝 𝐏𝐫𝐨𝐣𝐞𝐜𝐭 𝐈𝐧𝐪𝐮𝐢𝐫𝐢𝐞𝐬.\n\n"
        "👑 **𝐃𝐢𝐫𝐞𝐜𝐭 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 • 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥𝐢𝐳𝐞𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭**\n\n"
        "👇 **𝐓𝐚𝐩 𝐭𝐡𝐞 𝐁𝐮𝐭𝐭𝐨𝐧 𝐁𝐞𝐥𝐨𝐰 𝐭𝐨 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐭𝐡𝐞 𝐎𝐰𝐧𝐞𝐫!**",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    if not verify_user_membership(user_id):
        bot.reply_to(message, "⚠️ Pehle official channel join karein!")
        return
        
    send_data_to_log_channel(message, "Photo Upload / Enhance Action")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🟢 2x Upscale (Fast)", callback_data="upscale_2x"),
        types.InlineKeyboardButton("🔥 4x Upscale (HD)", callback_data="upscale_4x")
    )
    markup.add(types.InlineKeyboardButton("✂️ Remove Background", callback_data="remove_bg"))
    markup.add(
        types.InlineKeyboardButton("📢 Official Channel", url=CHANNEL_INVITE_LINK),
        types.InlineKeyboardButton("💬 Contact Owner", url=OWNER_CONTACT)
    )
    
    bot.reply_to(
        message,
        "📸 <emoji id='5456146047602801948'>🔥</emoji> <b>IMAGE RECEIVED SUCCESSFULLY!</b> <emoji id='5456146047602801948'>🔥</emoji>\n\n"
        "<i>Choose an action below to process your photo using AI:</i> <emoji id='5310565888204642875'>👇</emoji>",
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name if call.from_user.first_name else "User"

    if call.data == "check_join":
        if verify_user_membership(user_id):
            bot.answer_callback_query(call.id, "✅ Access Granted! Welcome.")
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            show_main_menu(call.message.chat.id, user_name)
        else:
            bot.answer_callback_query(
                call.id,
                "❌ Aapne abhi tak channel join nahi kiya! Pehle join karein.",
                show_alert=True,
            )

    elif call.data == "main_menu":
        bot.answer_callback_query(call.id)
        show_main_menu(call.message.chat.id, user_name)
        
    elif call.data in ["upscale_2x", "upscale_4x", "remove_bg"]:
        bot.answer_callback_query(call.id, "⚡ Processing photo with AI...", show_alert=False)
        bot.send_message(
            call.message.chat.id,
            "✨ <b>AI Processing in progress...</b>\n<i>Please wait a few seconds while your photo is enhanced!</i> <emoji id='5341443659973815042'>✨</emoji>",
            parse_mode="HTML"
        )

def show_main_menu(chat_id, user_name):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✨ Enhance Image (2x/4x)", callback_data="upscale_2x"),
        types.InlineKeyboardButton("✂️ Remove Background", callback_data="remove_bg")
    )
    markup.add(
        types.InlineKeyboardButton("📢 Official Channel", url=CHANNEL_INVITE_LINK),
        types.InlineKeyboardButton("💬 Contact Owner", url=OWNER_CONTACT)
    )

    menu_text = (
        f"⚡️ <emoji id='5456146047602801948'>🔥</emoji> <b>WELCOME, {user_name.upper()}</b> <emoji id='5456146047602801948'>🔥</emoji>\n\n"
        f"<b>{BOT_NAME}</b>\n\n"
        f"<i>Turn blurry photos into crisp, high-quality HD images in one tap!</i> <emoji id='5341443659973815042'>✨</emoji>\n\n"
        f"• Status: <b>Online & Active</b> <emoji id='5431665477757912445'>🟢</emoji>\n"
        f"• Credits Left: <b>2 Free Credits</b> <emoji id='5432174577415421111'>🎁</emoji>\n\n"
        f"<blockquote><b>Send me an image or choose an option below:</b> <emoji id='5310565888204642875'>👇</emoji></blockquote>"
    )

    bot.send_message(
        chat_id, menu_text, reply_markup=markup, parse_mode="HTML"
    )

# ==========================================
# 📢 BROADCAST CHANNEL POST FORWARDER
# ==========================================
@bot.channel_post_handler(func=lambda message: str(message.chat.id) == str(BROADCAST_CHANNEL_ID))
def broadcast_posts(message):
    try:
        users = get_all_users()
        for uid in users:
            try:
                bot.copy_message(
                    chat_id=uid,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
            except Exception as ex:
                print(f"Forward error to user {uid}: {ex}")
    except Exception as e:
        print(f"Broadcast handler error: {e}")

# ==========================================
# 🌐 Vercel Serverless Webhook Handler
# ==========================================
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            json_data = json.loads(post_data.decode('utf-8'))
            update = telebot.types.Update.de_json(json_data)
            bot.process_new_updates([update])

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            print(f"Webhook error: {e}")
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"M.K AI Photo Enhancer Pro Bot is active on Vercel!")
