import telebot
from ytmusicapi import YTMusic
import os
import youtube_dl


# Function to download YouTube video as an MP3 file and return the downloaded file path
def download_youtube_video(url, output_file):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_file # Specify the output file path
        
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
  
    return output_file

    # Function to remove a file
def remove_file(file_path):
    try:
        # Remove the file
        os.remove(file_path)
        print("File removed successfully:", file_path)
    except OSError as e:
        # Print an error message if the file removal fails
        print("Error occurred while removing the file:", e)


# Your bot token (replace 'YOUR_BOT_TOKEN' with the token obtained from BotFather)
TOKEN = 'YOUR_BOT_TOKEN'

# Create an instance of the bot
bot = telebot.TeleBot(TOKEN)

# Create an instance of the YTMusic API client
ytmusic = YTMusic()

# Define a command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, I'm your Telegram bot! Please send me the name of a song.")

# Define a message handler
@bot.message_handler(func=lambda message: True)
def search_and_get_link(message):
    song_name = message.text

    # Search for the song on YouTube Music
    search_results = ytmusic.search(query=song_name, filter="songs", limit=1)
    
    if search_results:
        bot.reply_to(message, f"w8 a minute!!")
        video_id = search_results[0]['videoId']
        song_link = f"https://music.youtube.com/watch?v={video_id}"
        
        Filebr=download_youtube_video(song_link,song_name+".mp3")
        bot.send_audio(message.chat.id,audio=open(Filebr, 'rb'))
    else:
        bot.reply_to(message, f"Sorry, I couldn't find any results for the song '{song_name}' on YouTube Music.")
    remove_file(Filebr)
# Start the bot
bot.polling()