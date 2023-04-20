import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube

# Define 6266282862:AAEaJj5srKV3L-bLpEpWGmUj_B_9iTuh59U
TOKEN = '6266282862:AAEaJj5srKV3L-bLpEpWGmUj_B_9iTuh59U'

# Define the function to handle the '/start' command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a bot that can download videos from YouTube. Just send me a YouTube video link and I'll do the rest!")

# Define the function to handle YouTube video links
def handle_video_link(update, context):
    # Get the YouTube video link from the user's message
    video_link = update.message.text
    
    # Check if the link is valid
    try:
        yt = YouTube(video_link)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, the link you provided is not valid.")
        return
    
    # Get the highest resolution stream of the video
    stream = yt.streams.get_highest_resolution()
    
    # Download the video to the working directory
    stream.download()
    
    # Send the downloaded video to the user
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(stream.default_filename, 'rb'))

# Define the main function
def main():
    # Create the Telegram bot updater and dispatcher
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Register the command and message handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    video_link_handler = MessageHandler(Filters.text & (~Filters.command), handle_video_link)
    dispatcher.add_handler(video_link_handler)
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
