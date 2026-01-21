import telebot
import requests
import time
import http.server
import socketserver
import threading
import os

# --- ១. កូដបង្កើត PORT ក្លែងក្លាយ (ដើម្បីឱ្យ Web Service ដើរ) ---
def start_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started at port {port}")
        httpd.serve_forever()

threading.Thread(target=start_server, daemon=True).start()

# --- ២. កូដបត TELEGRAM ---
API_TOKEN = '8511913164:AAEYjaIjnSoE_NGd2pSx_6-6fKl6AvbSg3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! ខ្ញុំគឺបតទាញយករបស់ Thearin\nផ្ញើ Link (FB, TikTok, YT, Kuaishou) មក ខ្ញុំដោនជូន!")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "សូមផ្ញើ Link ឱ្យបានត្រឹមត្រូវ។")
        return

    msg = bot.reply_to(message, "⏳ កំពុងទាញយក... សូមរង់ចាំបន្តិច!")

    try:
        api_url = f"https://api.vkrhost.info/api/download?url={url}"
        response = requests.get(api_url).json()

        if response.get("status"):
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="✅ ទាញយកជោគជ័យដោយ Thearin!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            api_url_2 = f"https://api.reallifetools.com/v1/download?url={url}"
            response_2 = requests.get(api_url_2).json()
            if response_2.get("success"):
                bot.send_video(message.chat.id, response_2["data"]["url"], caption="✅ ទាញយកជោគជ័យ!")
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ រកមិនឃើញវីដេអូទេ ឬ Link Private។", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("⚠️ Server កំពុងមមាញឹក សូមសាកល្បងម្ដងទៀត។", message.chat.id, msg.message_id)

bot.infinity_polling(timeout=20)
