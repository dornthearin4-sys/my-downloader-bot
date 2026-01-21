import telebot
import yt_dlp
import os

# លេខ Token របស់បងដែលបានមកពី BotFather
API_TOKEN = '8511913164:AAEF_nik_mx5q99FXw-ARdyu5Ht6SJ29Rco'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តីបង! ខ្ញុំគឺ Downloader By Thearin។ សូមផ្ញើ Link វីដេអូមក ខ្ញុំនឹងទាញយកជូន។")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, "កំពុងទាញយក... សូមរង់ចាំ!")
    
    try:
        # ការកំណត់សម្រាប់ទាញយកវីដេអូ
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # ផ្ញើវីដេអូទៅកាន់ Telegram របស់បង
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        # លុប File ចេញក្រោយផ្ញើរួចដើម្បីសន្សំទំហំផ្ទុក
        os.remove('video.mp4')
        
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហា៖ {str(e)}")

bot.polling()
