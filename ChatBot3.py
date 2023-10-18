# Create a telegram bot using openai ChatGPT
import os
import openai
import telegram
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

# obtain api keys
load_dotenv()
botKey = os.getenv("BOT_KEY")
telegramKey = os.getenv("TELEGRAM_BOT_KEY")

openai.api_key = botKey
TELEGRAM_API_TOKEN = telegramKey

# config messages
messages = [{"role": "system",
             "content": "You are a TelegramGPT, a helpful telegram bot that is always concise and polite in its answers."}]


def text_message(update, context):
    messages.append({"role": "user", "content": update.message.text})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    Bot_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(text=f"*[BOT]:* {Bot_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    # append to messages to let bot remember it
    messages.append({"role": "assistant", "content": Bot_reply})


# Set up telegram bot and dispatcher
updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
# Register message handler and pass in text_message function
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
# Start the bot
updater.start_polling()
updater.idle()
