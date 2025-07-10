import logging
import threading
import requests
import asyncio
from telegram.ext import Application, CommandHandler
from bs4 import BeautifulSoup
from datetime import datetime

# Konfiguracja logowania
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Token bota
TOKEN = "7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE"
URL = "https://telegram-bot1-eod3.onrender.com"
daily_tips = {}

# Funkcja do pobierania aktualnego czasu
def get_current_time():
    now = datetime.now()  # Pobiera aktualny czas
    return now.strftime("%Y-%m-%d %H:%M:%S")  # Format daty: Rok-Miesiąc-Dzień Godzina:Minuta:Sekunda

# Komendy
async def start(update, context):
    await update.message.reply_text("Bot działa!")

# Komenda /gram - do zmiany stawki
async def gram(update, context):
    if context.args:
        amount = context.args[0]
        await update.message.reply_text(f"Zmieniono stawkę na {amount} zł")
    else:
        await update.message.reply_text("Proszę podać kwotę, np. /gram 10zł")

# Komenda /niegram - do rezygnacji ze stawki
async def niegram(update, context):
    await update.message.reply_text("Zrezygnowano z obstawiania.")

# Komenda do wysyłania pewniaków z godziną
async def wyslij_typ(update, context):
    current_time = get_current_time()  # Pobiera aktualny czas
    typ = "Tenis: Zwycięzca meczu: XYZ, kurs 1.8"
    await update.message.reply_text(f"{typ}\nDodano o: {current_time}")  # Dodaje godzinę pod typem

# Funkcja pingująca, aby utrzymać bota aktywnego
def ping_self():
    try:
        requests.get(URL)
        print("Ping OK")
    except Exception as e:
        print(f"Ping failed: {e}")
    threading.Timer(600, ping_self).start()  # Ping co 600 sekund = 10 minut

# Funkcja do pobierania kursów z Betclick (przykładowe, musisz dostosować do strony)
def get_betclick_odds():
    url = "URL_DO_BETCLICK"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Załóżmy, że kursy są w divach z klasą 'odds'
    odds_elements = soup.find_all('div', class_='odds')
    odds = []
    for element in odds_elements:
        odds.append(element.text.strip())
    return odds

# Funkcja do wysyłania typów codziennie o określonej godzinie
async def send_daily_tips():
    while True:
        # Pobierz aktualne typy i wysyłaj
        await wyslij_typ(update, context)  # To jest przykład, musisz dostosować do swojej logiki
        await asyncio.sleep(21600)  # Czekaj 6 godzin

# Główna funkcja uruchamiająca bota
async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gram", gram))
    application.add_handler(CommandHandler("niegram", niegram))

    # Pingowanie co 10 minut
    ping_self()

    # Uruchomienie bota w tle
    job_queue = application.job_queue
    job_queue.run_repeating(wyslij_typ, interval=21600, first=5)

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
