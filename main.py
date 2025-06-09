import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

API_URL = "https://api.llama.fi/chat/completions"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! اسأل أي شيء وسأجيبك بحرية 🎯")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("حدث خطأ أثناء معالجة رسالتك.")

app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
