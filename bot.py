import logging
import requests
import random
import time
import os
from bs4 import BeautifulSoup
from telegram.ext import Application, CommandHandler
from datetime import datetime

# Ustaw loggera
logging.basicConfig(level=logging.INFO)

# Token bota
TOKEN = '7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE'

# Lista typów
typy = []

# Komendy
async def start(update, context):
    await update.message.reply_text("👋 Cześć! Wpisz /gram 10zł lub /niegram albo /dlaczego")

async def gram(update, context):
    amount = context.args[0] if context.args else '?'
    await update.message.reply_text(f"✅ Zapisano: grasz {amount} zł. Dzięki!")

async def niegram(update, context):
    await update.message.reply_text("❌ OK, nie grasz. Może później coś ci się spodoba!")

async def dlaczego(update, context):
    await update.message.reply_text("🤖 Typy są wybierane dzięki analizie statystyk i gry na podstawie dostępnych danych.")

# Funkcja główna do typów
def scrape_typy():
    return [
        {"mecz": "Nadal vs Djokovic", "typ": "Nadal wygra", "kurs": 1.82},
        {"mecz": "Świątek vs Gauff", "typ": "Świątek -1.5 seta", "kurs": 2.05}
    ]

# Funkcja do wysyłania typów
async def wyslij_typy(application):
    global typy
    typy_dnia = scrape_typy()
    numer = 1
    for typ in typy_dnia:
        if typ["kurs"] >= 1.75:
            msg = f"🎾 Typ nr {numer}:\nMecz: {typ['mecz']}\nTyp: {typ['typ']}\nKurs: {typ['kurs']}"
            for chat_id in application.chat_ids:
                await application.bot.send_message(chat_id=chat_id, text=msg)
            numer += 1
    typy = typy_dnia

# Start bota
async def main():
    app = Application.builder().token(TOKEN).build()

    app.chat_ids = set()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gram", gram))
    app.add_handler(CommandHandler("niegram", niegram))
    app.add_handler(CommandHandler("dlaczego", dlaczego))

    print("🤖 Bot działa...")

    await app.start()
    await app.updater.start_polling()

    while True:
        await wyslij_typy(app)
        await asyncio.sleep(600)

import asyncio
if __name__ == '__main__':
    asyncio.run(main())
