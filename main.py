import telebot
import requests
import os

# Token របស់បង
API_TOKEN = '8511913164:AAEF_nik_mx5q99FXw-ARdyu5Ht6SJ29Rco'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "សួស្តីបង! ខ្ញុំគឺបតទាញយកវីដេអូរបស់ Thearin\n\n"
        "បងអាចផ្ញើ Link មកពី៖\n"
        "✅ Facebook\n"
        "✅ TikTok (អត់ Watermark)\n"
        "✅ YouTube\n"
        "✅ Kuaishou (快手)\n\n"
        "សូមផ្ញើ Link មកឥឡូវនេះ!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "សូមផ្ញើ Link ឱ្យបានត្រឹមត្រូវ។")
        return

    processing_msg = bot.reply_to(message, "កំពុងទាញយក... សូមរង់ចាំបន្តិច!")

    try:
        # ប្រើ API រួមដែលធានាថាអាចដោនបានគ្រប់ App
        api_url = f"https://api.vkrhost.info/api/download?url={url}"
        response = requests.get(api_url).json()

        if response.get("status"):
            # រើសយក Link វីដេអូដែលច្បាស់ជាងគេ
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="ទាញយកជោគជ័យដោយ Thearin")
            bot.delete_message(message.chat.id, processing_msg.message_id)
        else:
            bot.edit_message_text("រកមិនឃើញវីដេអូទេ ឬ Link មិនត្រឹមត្រូវ។", message.chat.id, processing_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"មានបញ្ហា៖ {str(e)}", message.chat.id, processing_msg.message_id)

bot.infinity_polling(timeout=10, long_polling_timeout=5)
