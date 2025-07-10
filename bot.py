import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random

logging.basicConfig(level=logging.INFO)
TOKEN = '7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE'

# Lista typów testowych
typy_testowe = [
    {"mecz": "Nadal vs Djokovic", "typ": "Nadal wygra", "kurs": 1.82},
    {"mecz": "Świątek vs Gauff", "typ": "Świątek -1.5 seta", "kurs": 2.05}
]

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Cześć! Wpisz /gram 10zł lub /niegram albo /dlaczego")

# Gram
async def gram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kwota = context.args[0] if context.args else "?"
    await update.message.reply_text(f"✅ Zapisano: grasz {kwota} zł")

# Nie gram
async def niegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ OK, może następnym razem!")

# Dlaczego
async def dlaczego(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Typy są wybierane na podstawie danych i analizy statystyk.")

# Wysyłanie typów
async def wyslij_typy(application):
    while True:
        for i, typ in enumerate(typy_testowe, start=1):
            if typ["kurs"] >= 1.75:
                tekst = f"🎾 Typ nr {i}:\nMecz: {typ['mecz']}\nTyp: {typ['typ']}\nKurs: {typ['kurs']}"
                for chat_id in application.chat_ids:
                    await application.bot.send_message(chat_id=chat_id, text=tekst)
        await asyncio.sleep(600)

# Główna funkcja
async def main():
    application = Application.builder().token(TOKEN).build()
    application.chat_ids = set()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gram", gram))
    application.add_handler(CommandHandler("niegram", niegram))
    application.add_handler(CommandHandler("dlaczego", dlaczego))

    # Uruchom bota
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    asyncio.create_task(wyslij_typy(application))
    await application.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
