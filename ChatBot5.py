# voice to machine voice bot in telegram
import os
import telegram
import openai
from moviepy.editor import AudioFileClip
from telegram.ext import Updater, MessageHandler, Filters
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("BOT_KEY")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_BOT_KEY")

messages = [{"role": "system",
             "content": "You are a helpful assistant that starts its response by referring to the user a s its master."}]


def text_message(update, context):
    update.message.reply_text(
        "I've received a text message! Please give me a second to respond :)")
    messages.append({"role": "user", "content": update.message.text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    tts = gTTS(text=response_text, lang='en')
    tts.save('response_gtts.mp3')
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_gtts.mp3', 'rb'))
    update.message.reply_text(
        text=f"*[Bot]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response_text})


def voice_message(update, context):
    update.message.reply_text(
        "I've received a voice message! Please give me a second to respond :)")
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    update.message.reply_text(
        text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    tts = gTTS(text=response_text, lang='en')
    # Save the audio to a file
    tts.save('response_gtts.mp3')
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_gtts.mp3', 'rb'))
    update.message.reply_text(
        text=f"*[Bot]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response_text})


updater = Updater(TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(
    Filters.text & (~Filters.command), text_message))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
updater.start_polling()
updater.idle()
