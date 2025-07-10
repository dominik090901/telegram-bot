import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Wstaw tu swój token
TOKEN = "7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE"

# Konfiguracja logowania
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Stan użytkownika
user_state = {}

# Komenda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Użyj /gram 10zł, /niegram lub /dlaczego")

# Komenda /gram
async def gram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        kwota = context.args[0]
        user_state[user_id] = {"gra": True, "kwota": kwota}
        await update.message.reply_text(f"OK, grasz za {kwota}")
    else:
        await update.message.reply_text("Podaj kwotę np. /gram 10zł")

# Komenda /niegram
async def niegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = {"gra": False}
    await update.message.reply_text("OK, nie grasz")

# Komenda /dlaczego
async def dlaczego(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bo ten typ wygląda bardzo pewnie na podstawie statystyk!")

# Główna funkcja uruchamiająca bota
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gram", gram))
    app.add_handler(CommandHandler("niegram", niegram))
    app.add_handler(CommandHandler("dlaczego", dlaczego))

    app.run_polling()

if __name__ == "__main__":
    main()
