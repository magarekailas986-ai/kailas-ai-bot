from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import requests
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

API_KEY = os.getenv("API_KEY")

users = set()


def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",

        "messages": [

            {
                "role": "system",

                "content": (
                    "You are Kailas AI.\n"
                    "You help users in English, Hindi, and Roman Hindi.\n"
                    "Reply in the same language style as the user.\n"
                    "Keep explanations simple and useful.\n"
                    "Help students, creators, and beginners.\n"
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    users.add(user_id)

    await update.message.reply_text(
        "🔥 Kailas AI Activated 🔥\n\n"

        "Languages:\n"
        "✅ English\n"
        "✅ Hindi\n"
        "✅ Roman Hindi\n\n"

        "Commands:\n"
        "/help\n"
        "/idea\n"
        "/summary\n"
        "/caption\n"
        "/mcq\n"
        "/explain\n"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Commands:\n\n"

        "/idea - AI business idea\n"

        "/summary - summarize text\n"

        "/caption - Instagram caption\n"

        "/mcq - create MCQs\n"

        "/explain - explain simply\n"

        "/help - command list\n\n"

        "Examples:\n"

        "/caption AI is changing the world\n"

        "/mcq photosynthesis\n"

        "/explain black hole"
    )


async def idea_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    prompt = (
        "Give one practical AI startup or business idea "
        "for beginners."
    )

    ai_reply = ask_ai(prompt)

    await update.message.reply_text(ai_reply)


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = " ".join(context.args)

    if not text:

        await update.message.reply_text(
            "Usage:\n/summary your text"
        )

        return

    prompt = (
        f"Summarize this simply:\n\n{text}"
    )

    ai_reply = ask_ai(prompt)

    await update.message.reply_text(ai_reply)


async def caption_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = " ".join(context.args)

    if not text:

        await update.message.reply_text(
            "Usage:\n/caption topic"
        )

        return

    prompt = (
        f"Create a powerful Instagram caption about:\n\n{text}"
    )

    ai_reply = ask_ai(prompt)

    await update.message.reply_text(ai_reply)


async def mcq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = " ".join(context.args)

    if not text:

        await update.message.reply_text(
            "Usage:\n/mcq topic"
        )

        return

    prompt = (
        f"Create 5 MCQs with answers about:\n\n{text}"
    )

    ai_reply = ask_ai(prompt)

    await update.message.reply_text(ai_reply)


async def explain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = " ".join(context.args)

    if not text:

        await update.message.reply_text(
            "Usage:\n/explain topic"
        )

        return

    prompt = (
        f"Explain this in simple language:\n\n{text}"
    )

    ai_reply = ask_ai(prompt)

    await update.message.reply_text(ai_reply)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    ai_reply = ask_ai(user_message)

    await update.message.reply_text(ai_reply)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("help", help_command))

app.add_handler(CommandHandler("idea", idea_command))

app.add_handler(CommandHandler("summary", summary_command))

app.add_handler(CommandHandler("caption", caption_command))

app.add_handler(CommandHandler("mcq", mcq_command))

app.add_handler(CommandHandler("explain", explain_command))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("🔥 Kailas AI Running 🔥")

app.run_polling()
