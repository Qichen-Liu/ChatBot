# a human-sound voice chatbot
import os
import openai
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
import telegram
from moviepy.editor import AudioFileClip
from elevenlabslib import *

load_dotenv()
openai.api_key = os.getenv("BOT_KEY")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_BOT_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# config elevenlab user voice
user = ElevenLabsUser(ELEVENLABS_API_KEY)
# This is a list because multiple voices can have the same name
voice = user.get_voices_by_name("Bella")[0]

messages = [{"role": "system",
             "content": "You are an English teacher who teach international students spoken English and grammar."}]


def text_message(update, context):
    update.message.reply_text(
        "I've received a text message! Please give me a second to respond :)"
    )
    messages.append({"role": "user", "content": update.message.text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": response_text})
    # call elevenlab api
    response_byte_audio = voice.generate_audio_bytes(response_text)

    with open('response_elevenlabs.mp3', 'wb') as f:
        f.write(response_byte_audio)

    context.bot.send_voice(chat_id=update.message.chat.id, voice=open('response_elevenlabs.mp3', 'rb'), timeout=100)
    update.message.reply_text(
        text=f"*[Bot]:* {response_text}",
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def voice_message(update, context):
    update.message.reply_text(
        "I've received a voice message! Please give me a second to respond :)"
    )
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")

    # TODO: test other api that do not require file in local
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    update.message.reply_text(text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    response_byte_audio = voice.generate_audio_bytes(response_text)
    with open('response_elevenlabs.mp3', 'wb') as f:
        f.write(response_byte_audio)
    # send voice message
    # TODO: check if not write the file to local
    context.bot.send_voice(chat_id=update.message.chat.id, voice=open('response_elevenlabs.mp3', 'rb'), timeout=100)
    # can choose not to send the message
    update.message.reply_text(text=f"*[Bot]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response_text})


updater = Updater(TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
updater.start_polling()
updater.idle()
