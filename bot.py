import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE'

# Włącz logowanie
logging.basicConfig(level=logging.INFO)

# Testowe typy
typy = [
    {"mecz": "Djokovic vs Alcaraz", "typ": "Djokovic wygra", "kurs": 1.85},
    {"mecz": "Świątek vs Rybakina", "typ": "Świątek -1.5 seta", "kurs": 2.10}
]

chat_ids = set()
typ_counter = 0

# Komenda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_ids.add(update.effective_chat.id)
    await update.message.reply_text("👋 Cześć! Wpisz /gram 10zł, /niegram albo /dlaczego")

# Komenda /gram
async def gram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(f"✅ Zapisano: grasz {context.args[0]}")
    else:
        await update.message.reply_text("Podaj kwotę, np. /gram 10zł")

# Komenda /niegram
async def niegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ OK, zapisano że nie grasz.")

# Komenda /dlaczego
async def dlaczego(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Typy są wybierane na podstawie danych i analizy statystyk.")

# Wysyłanie typów (co 10 minut przykładowo)
async def wysylaj_typy(application):
    global typ_counter
    while True:
        for typ in typy:
            typ_counter += 1
            tekst = f"🎾 Typ nr {typ_counter}:\nMecz: {typ['mecz']}\nTyp: {typ['typ']}\nKurs: {typ['kurs']}"
            for chat_id in chat_ids:
                await application.bot.send_message(chat_id=chat_id, text=tekst)
        await asyncio.sleep(600)  # co 10 minut

# Główna funkcja
async def main():
    application = Application.builder().token(TOKEN).build()

    # Komendy
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gram", gram))
    application.add_handler(CommandHandler("niegram", niegram))
    application.add_handler(CommandHandler("dlaczego", dlaczego))

    # Uruchomienie
    asyncio.create_task(wysylaj_typy(application))
    await application.run_polling()

# Uruchomienie (Render wymaga asyncio.run)
if __name__ == "__main__":
    asyncio.run(main())
