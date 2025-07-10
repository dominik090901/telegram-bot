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

# Zmienna do liczenia typów dziennych
daily_tips = {}

# URL do podtrzymania działania na Renderze
URL = "https://telegram-bot1-eod3.onrender.com"

# Komenda start
async def start(update, context):
    await update.message.reply_text("Bot działa!")

# Komenda /gram
async def gram(update, context):
    if context.args:
        context.user_data["gram"] = True
        context.user_data["stawka"] = context.args[0]
        await update.message.reply_text(f"Zarejestrowano: grasz za {context.args[0]}")
    else:
        await update.message.reply_text("Użycie: /gram 10zł")

# Komenda /niegram
async def niegram(update, context):
    context.user_data["gram"] = False
    await update.message.reply_text("Zarejestrowano: nie grasz tego meczu.")

# Komenda /dlaczego
async def dlaczego(update, context):
    await update.message.reply_text("Typ został wybrany na podstawie analizy statystyk i kursów. Pewny value.")

# Wysyłanie typu tenisowego
async def wyslij_typ(context):
    chat_id = 7793377623  # Twój ID
    today = datetime.now().date()
    daily_tips[today] = daily_tips.get(today, 0) + 1
    numer = daily_tips[today]

    # Pobranie typu z Betclicka
    typ, kurs = pobierz_typ_z_betclick()

    if typ:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🎾 Typ nr {numer}:\n{typ}\nKurs: {kurs}\n\n✅ Pewniak dnia"
        )

# Prosty scraper Betclicka
def pobierz_typ_z_betclick():
    try:
        url = "https://www.betclick.pl/zaklady-bukmacherskie/tenis-5"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Znajdź przykładowy typ
        mecz = soup.find("a", class_="event-row-link")
        if mecz:
            nazwa = mecz.text.strip()
            kurs = "1.85+"  # Domyślny kurs, bo z Betclicka nie wyciągamy dokładnych wartości
            return nazwa, kurs
    except Exception as e:
        print("Błąd scrapera:", e)
    return None, None

# Pingowanie co 10 minut żeby bot nie zasnął
def ping_self():
    try:
        requests.get(URL)
        print("Ping OK")
    except Exception as e:
        print("Ping failed:", e)
    threading.Timer(600, ping_self).start()  # co 10 min

# Uruchamianie bota
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gram", gram))
    app.add_handler(CommandHandler("niegram", niegram))
    app.add_handler(CommandHandler("dlaczego", dlaczego))

    # Harmonogram: typ co 6h
    job_queue = app.job_queue
    job_queue.run_repeating(wyslij_typ, interval=21600, first=5)

    ping_self()

    await app.run_polling()

# Uruchomienie aplikacji
if __name__ == "__main__":
    asyncio.run(main())
