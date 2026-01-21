import telebot
import requests
import time

# លេខ Token របស់បង (បងអាចប្រើលេខចាស់ ឬ Revoke យកលេខថ្មីកាន់តែល្អ)
API_TOKEN = '8511913164:AAEF_nik_mx5q99FXw-ARdyu5Ht6SJ29Rco'
bot = telebot.TeleBot(API_TOKEN)

# ការពារការជាន់គ្នា
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
        # API ពិសេសដែល Support គ្រប់ App
        api_url = f"https://api.vkrhost.info/api/download?url={url}"
        response = requests.get(api_url).json()
        
        if response.get("status"):
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="ទាញយកជោគជ័យដោយ Thearin!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("រកមិនឃើញវីដេអូទេ ឬ Link ខុស។", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"បញ្ហា៖ {str(e)}", message.chat.id, msg.message_id)

bot.infinity_polling(timeout=20, long_polling_timeout=10)
