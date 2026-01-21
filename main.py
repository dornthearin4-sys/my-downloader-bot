import telebot
import requests
import time
import http.server
import socketserver
import threading
import os

# --- ១. កូដបង្កើត PORT ក្លែងក្លាយ (សម្រាប់ឱ្យ Render ដាក់ LIVE លឿន) ---
def start_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=start_server, daemon=True).start()

# --- ២. កូដបត TELEGRAM ---
API_TOKEN = '8511913164:AAEYjaIjnSoE_NGd2pSx_6-6fKl6AvbSg3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! បតដោនវីដេអូ Thearin ជំនាន់ Pro ដំណើរការហើយ!\nផ្ញើ Link (FB, TikTok, IG, YT) មក ខ្ញុំដោនជូន!")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "សូមផ្ញើ Link ឱ្យបានត្រឹមត្រូវបង។")
        return

    msg = bot.reply_to(message, "⏳ កំពុងឆែកមើល Server ទាំង ៣... សូមរង់ចាំ!")

    # មុខងារជំនួយសម្រាប់ទាញយក (Try multi-API)
    def try_download(link):
        # --- សាក API ទី១ (vkrhost) ---
        try:
            res = requests.get(f"https://api.vkrhost.info/api/download?url={link}", timeout=10).json()
            if res.get("status"): return res["data"]["url"]
        except: pass

        # --- សាក API ទី២ (reallifetools) ---
        try:
            res = requests.get(f"https://api.reallifetools.com/v1/download?url={link}", timeout=10).json()
            if res.get("success"): return res["data"]["url"]
        except: pass
        
        # --- សាក API ទី៣ (Tikwm - ពិសេសសម្រាប់ TikTok) ---
        if "tiktok.com" in link:
            try:
                res = requests.get(f"https://www.tikwm.com/api/?url={link}", timeout=10).json()
                if res.get("data"): return "https://www.tikwm.com" + res["data"]["play"]
            except: pass
            
        return None

    video_url = try_download(url)

    if video_url:
        try:
            bot.send_video(message.chat.id, video_url, caption="✅ ទាញយកជោគជ័យដោយ Thearin!")
            bot.delete_message(message.chat.id, msg.message_id)
        except:
            bot.edit_message_text("⚠️ វីដេអូធំពេក មិនអាចផ្ញើតាម Telegram បានទេ!", message.chat.id, msg.message_id)
    else:
        bot.edit_message_text("❌ Server ទាំង ៣ រវល់ខ្លាំងពេក! សូមសាកល្បងម្ដងទៀតនៅបន្តិចទៀតនេះ។", message.chat.id, msg.message_id)

bot.infinity_polling()
