import os
import requests
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

def start(update, context):
    update.message.reply_text("Hello Kailas 😄 AI Bot online hai!")

def reply(update, context):
    user_message = update.message.text

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    try:
        bot_reply = response.json()["choices"][0]["message"]["content"]
    except:
        bot_reply = "Error aa gaya 😅"

    update.message.reply_text(bot_reply)

updater = Updater(BOT_TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text, reply))

print("Bot chal raha hai 😄")

updater.start_polling()
updater.idle()
