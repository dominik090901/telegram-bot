import logging
from telegram.ext import Application, CommandHandler

# Funkcja na komendę /start
async def start(update, context):
    await update.message.reply_text("Bot działa!")

# Ustawienia logowania (pomocne do debugowania)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Wklej swój TOKEN z BotFather
TOKEN = "TU_WKLEJ_TOKEN"

# Tworzymy aplikację i handler
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Bot działa w pętli 24/7
app.run_polling()
