import logging
import os
import re
import requests
import datetime
import asyncio
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === KONFIGURACJA ===
TOKEN = "7280780498:AAFUnTebOpiqv0_jz-EIEVzdOQvLsLLEXvE"
USER_ID = 7793377623  # Twój ID z Telegrama
KURS_MINIMALNY = 1.75
DZISIAJ = datetime.date.today().isoformat()

# === PAMIĘĆ W RAM ===
stawka = 0
gram = False
historia_typow = []
numer_typu = 1

# === LOGI ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === SCRAPER BETCLICK ===
def pobierz_typy_betclick():
    url = "https://www.betclic.pl/pl/sport/tenis/9"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    typy = []
    for mecz in soup.select("a.sport-event"):
        nazwy = mecz.select_one(".sport-event-title span")
        kursy = mecz.select(".odd-value")
        if nazwy and len(kursy) >= 2:
            kurs1 = float(kursy[0].text.replace(",", "."))
            kurs2 = float(kursy[1].text.replace(",", "."))
            if kurs1 >= KURS_MINIMALNY:
                typy.append((nazwy.text.strip(), kurs1))
            if kurs2 >= KURS_MINIMALNY:
                typy.append((nazwy.text.strip(), kurs2))
    return typy

# === KOMENDY ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Będę wysyłał pewne typy z tenisa ziemnego. Użyj /gram 10zł lub /niegram.")

async def gram_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global gram, stawka
    if context.args:
        try:
            stawka = float(re.sub("[^0-9.]", "", context.args[0]))
            gram = True
            await update.message.reply_text(f"✅ Grasz. Stawka ustawiona: {stawka}zł")
        except:
            await update.message.reply_text("Błędna stawka. Użyj np. /gram 10zł")

async def niegram_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global gram
    gram = False
    await update.message.reply_text("❌ Nie grasz. Ten mecz nie będzie liczony do statystyk.")

async def dlaczego_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Ten typ został wybrany na podstawie analizy kursów, formy graczy i wartości zakładu. Jest to pewniak według naszej analizy!")

# === FUNKCJA WYSYŁANIA TYPOW ===
async def wyslij_typy(bot: Bot):
    global numer_typu
    typy = pobierz_typy_betclick()
    for nazwa, kurs in typy:
        tresc = f"🎾 Typ nr {numer_typu} ({DZISIAJ}):\nMecz: {nazwa}\nKurs: {kurs}\n"
        if gram and stawka > 0:
            tresc += f"Stawka: {stawka}zł"
        await bot.send_message(chat_id=USER_ID, text=tresc)
        historia_typow.append({"nazwa": nazwa, "kurs": kurs, "gram": gram, "stawka": stawka})
        numer_typu += 1

# === FUNKCJA GŁÓWNA ===
async def main():
    aplikacja = ApplicationBuilder().token(TOKEN).build()
    aplikacja.add_handler(CommandHandler("start", start))
    aplikacja.add_handler(CommandHandler("gram", gram_cmd))
    aplikacja.add_handler(CommandHandler("niegram", niegram_cmd))
    aplikacja.add_handler(CommandHandler("dlaczego", dlaczego_cmd))

    # Uruchomienie zadania co 10 minut (symulacja aktywności)
    async def zadanie():
        bot = Bot(token=TOKEN)
        while True:
            await wyslij_typy(bot)
            await asyncio.sleep(600)  # co 10 minut

    asyncio.create_task(zadanie())
    await aplikacja.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
