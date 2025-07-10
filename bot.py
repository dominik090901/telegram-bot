import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Funkcja na komendę /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot działa!")

# Ustawienia logowania
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# TOKEN z BotFather
TOKEN = "TU_WKLEJ_TOKEN"  # <-- tutaj wklej swój prawdziwy token

# Główna funkcja asynchroniczna
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot wystartował! ✅")
    await app.run_polling()

# Uruchomienie bota
if __name__ == "__main__":
    asyncio.run(main())
