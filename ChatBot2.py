# chatgpt with gradio
import os
import openai
import gradio
from dotenv import load_dotenv, dotenv_values

load_dotenv()
botKey = os.getenv("BOT_KEY")
openai.api_key = botKey

# config the bot
messages = [{"role": "system", "content": "You are a software engineering tech recruiter"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    # call ChatGPT to get response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    # messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

# use gradio to create a simple UI
demo = gradio.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="My Interview Trainer")

demo.launch(share=True)
