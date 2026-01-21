import telebot
import requests
import os

# លេខ Token របស់បងដែលបានមកពី BotFather
API_TOKEN = '8511913164:AAEF_nik_mx5q99FXw-ARdyu5Ht6SJ29Rco'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! ខ្ញុំគឺបតទាញយកវីដេអូរបស់ Thearin។\nសូមផ្ញើ Link (FB, TikTok, YT, Kuaishou) មក ខ្ញុំនឹងទាញយកជូន។")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "សូមផ្ញើ Link ឱ្យត្រឹមត្រូវ។")
        return

    msg = bot.reply_to(message, "កំពុងទាញយក... សូមរង់ចាំ!")

    try:
        # ប្រើប្រាស់ API រួមដើម្បីទាញយកគ្រប់ App
        api_url = f"https://api.vkrhost.info/api/download?url={url}"
        response = requests.get(api_url).json()

        if response.get("status"):
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="ទាញយកដោយជោគជ័យដោយ Thearin!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("រកមិនឃើញវីដេអូទេ ឬ Link ខុស។", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"បញ្ហា៖ {str(e)}", message.chat.id, msg.message_id)

# បញ្ជៀសបញ្ហា Conflict (Error 409)
bot.infinity_polling(timeout=10, long_polling_timeout=5)
