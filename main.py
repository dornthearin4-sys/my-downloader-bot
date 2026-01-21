import telebot
import requests
import time
import http.server
import socketserver
import threading
import os

# ១. បង្កើត Port ក្លែងក្លាយដើម្បីឱ្យ Render ដាក់ថា Live
def start_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=start_server, daemon=True).start()

# ២. កូដបត Telegram (Token ថ្មីរបស់បង)
API_TOKEN = '8511913164:AAEYjaIjnSoE_NGd2pSx_6-6fKl6AvbSg3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! បតដោនវីដេអូ Thearin ដំណើរការហើយ!\nផ្ញើ Link មក ខ្ញុំដោនជូន!")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    msg = bot.reply_to(message, "⏳ កំពុងទាញយក... សូមរង់ចាំ!")
    try:
        # សាក API ១
        res = requests.get(f"https://api.vkrhost.info/api/download?url={url}").json()
        if res.get("status"):
            bot.send_video(message.chat.id, res["data"]["url"], caption="✅ រួចរាល់!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            # សាក API ២
            res2 = requests.get(f"https://api.reallifetools.com/v1/download?url={url}").json()
            if res2.get("success"):
                bot.send_video(message.chat.id, res2["data"]["url"], caption="✅ រួចរាល់!")
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ រកមិនឃើញវីដេអូទេ!", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("⚠️ Server មមាញឹក សាកម្ដងទៀតណា!", message.chat.id, msg.message_id)

bot.infinity_polling()
