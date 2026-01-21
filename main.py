import telebot
import requests
import time

# លេខ Token ថ្មីរបស់បង (ពី BotFather)
API_TOKEN = '8511913164:AAEYjaIjnSoE_NGd2pSx_6-6fKl6AvbSg3c'
bot = telebot.TeleBot(API_TOKEN)

# ផ្ដាច់ការភ្ជាប់ចាស់ៗដែលនៅសេសសល់ដើម្បីសុវត្ថិភាព
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! ខ្ញុំគឺបតទាញយករបស់ Thearin\nផ្ញើ Link (FB, TikTok, YT, Kuaishou) មក ខ្ញុំដោនជូន!")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "សូមផ្ញើ Link ឱ្យបានត្រឹមត្រូវ។")
        return

    msg = bot.reply_to(message, "កំពុងទាញយក... សូមរង់ចាំ!")

    try:
        # ប្រើ API ថ្មីដែលរឹងមាំ និង Support គ្រប់ App
        api_url = f"https://api.reallifetools.com/v1/download?url={url}"
        response = requests.get(api_url).json()

        if response.get("success"):
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="ទាញយកជោគជ័យដោយ Thearin!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("រកមិនឃើញវីដេអូទេ ឬ Link មិនទាន់ Support។", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("Server កំពុងមមាញឹក សូមសាកល្បងម្ដងទៀត។", message.chat.id, msg.message_id)

bot.infinity_polling(timeout=20, long_polling_timeout=10)
