import logging
from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("Bot działa!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = "7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE"

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()import threading
import requests

# Adres Twojego bota na Render
URL = "https://telegram-bot1-eod3.onrender.com"

# Funkcja do pingowania co 10 minut
def ping_self():
    try:
        requests.get(https://telegram-bot1-eod3.onrender.com)
        print("Ping OK")
    except Exception as e:
        print("Ping failed:", e)
    threading.Timer(600, ping_self).start()  # ping co 600 sekund = 10 min

# Uruchom pingowanie
ping_self()

