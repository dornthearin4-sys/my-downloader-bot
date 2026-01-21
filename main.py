import telebot
import requests
import time

# លេខ Token ថ្មីបំផុតរបស់បង
API_TOKEN = '8511913164:AAEYjaIjnSoE_NGd2pSx_6-6fKl6AvbSg3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! ខ្ញុំគឺបតទាញយករបស់ Thearin\nសូមផ្ញើ Link (FB, TikTok, YT, Kuaishou) មក ខ្ញុំដោនជូន!")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "សូមផ្ញើ Link ឱ្យបានត្រឹមត្រូវ។")
        return

    msg = bot.reply_to(message, "⏳ កំពុងទាញយក... សូមរង់ចាំបន្តិច!")

    try:
        # ប្រើប្រាស់ API ទី១
        api_url = f"https://api.vkrhost.info/api/download?url={url}"
        response = requests.get(api_url).json()

        if response.get("status"):
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="✅ ទាញយកជោគជ័យដោយ Thearin!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            # បើសាក API ទី១ មិនបាន វានឹងសាក API ទី២ ភ្លាម
            api_url_2 = f"https://api.reallifetools.com/v1/download?url={url}"
            response_2 = requests.get(api_url_2).json()
            if response_2.get("success"):
                video_url_2 = response_2["data"]["url"]
                bot.send_video(message.chat.id, video_url_2, caption="✅ ទាញយកជោគជ័យដោយ Thearin!")
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ រកមិនឃើញវីដេអូក្នុង Link នេះទេ ឬវាជាវីដេអូ Private។", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ បច្ចុប្បន្ន Server កំពុងមមាញឹកខ្លាំង សូមសាកល្បងម្ដងទៀតនៅបន្តិចទៀតនេះ។", message.chat.id, msg.message_id)

bot.infinity_polling(timeout=20, long_polling_timeout=10)
