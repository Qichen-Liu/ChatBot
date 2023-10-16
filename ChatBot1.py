# chatgpt inside a infinite loop
import os
import openai
from dotenv import load_dotenv, dotenv_values

load_dotenv()
botKey = os.getenv("BOT_KEY")
openai.api_key = botKey

messages = []
print("what type of chatbot would you like to create?")
system_msg = input()
messages.append({"role":"user", "content":"system_msg"})

print("Your new assistant is ready")

while input != "quit":
    message = input()
    if message == "quit":
        break
    messages.append({"role":"user", "content":message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role":"assistant", "content":reply})
    print("\n" + reply + "\n")