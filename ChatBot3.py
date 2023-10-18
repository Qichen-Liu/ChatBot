# Create a telegram bot using openai ChatGPT
import os
import openai
from dotenv import load_dotenv, dotenv_values
from telegram.ext import Updater, MessageHandler, Filters

# obtain api keys
load_dotenv()
botKey = os.getenv("BOT_KEY")
telegramKey = os.getenv("TELEGRAM_BOT_KEY")

openai.api_key = botKey
TELEGRAM_API_TOKEN = telegramKey

def text_message(update, context):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role" : "system", "content" : "Always response with a random joke"}]
    )
    update.message.reply_text(response["choices"][0]["message"]["content"])

# Set up telegram bot and dispatcher
updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
# Register message handler and pass in text_message function
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
# Start the bot
updater.start_polling()
updater.idle()
