import logging
import threading
import requests
import asyncio
import os
from telegram.ext import Application, CommandHandler
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask

# Konfiguracja logowania
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Token bota
TOKEN = "7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE"
URL = "https://telegram-bot1-eod3.onrender.com"
daily_tips = {}

# Komendy
async def start(update, context):
    await update.message.reply_text("Bot działa!")

async def gram(update, context):
    if context.args:
        try:
            amount = float(context.args[0])
            await update.message.reply_text(f"Stawka: {amount} zł została zarejestrowana.")
        except ValueError:
            await update.message.reply_text("Wprowadź poprawną kwotę (np. /gram 10).")
    else:
        await update.message.reply_text("Proszę podać kwotę stawki (np. /gram 10).")

async def niegram(update, context):
    await update.message.reply_text("Nie gram!")

async def dlaczego(update, context):
    await update.message.reply_text("Bot analizuje statystyki i typy na podstawie dostępnych danych.")

# Funkcja pingowania do 10 minut
def ping_self():
    try:
        requests.get(URL)
        print("Ping OK")
    except Exception as e:
        print(f"Ping failed: {e}")
    threading.Timer(600, ping_self).start()  # ping co 600 sekund = 10 minut

# Uruchom pingowanie
ping_self()

# Tworzenie aplikacji bota
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gram", gram))
app.add_handler(CommandHandler("niegram", niegram))
app.add_handler(CommandHandler("dlaczego", dlaczego))

# Funkcja nasłuchująca na porcie Render
def run_flask():
    flask_app = Flask(__name__)

    @flask_app.route("/")
    def home():
        return "Bot działa!"

    # Nasłuchiwanie na porcie, który Render ustawia
    port = int(os.environ.get("PORT", 8080))  # domyślny port to 8080
    flask_app.run(host="0.0.0.0", port=port)

# Uruchomienie aplikacji bota w tle
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(app.run_polling())
    run_flask()  # Uruchomienie Flask, aby Render mógł nasłuchiwać na porcie
