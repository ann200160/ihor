import asyncio
import logging
import random
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import gspread

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Твій токен від BotFather
TOKEN = "8961643403:AAEjGi3G482HtvxR1CFyF-YMErsoVlJo3DI"

# Налаштування Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Безпечне завантаження ключа з Secret File на Render або локального файлу
secret_file_path = "/etc/secrets/credentials.json"

if os.path.exists(secret_file_path):
    gc = gspread.service_account(filename=secret_file_path, scopes=scope)
elif os.path.exists("credentials.json"):
    gc = gspread.service_account(filename="credentials.json", scopes=scope)
else:
    # Запасний варіант, якщо файл передається через словник
    raise FileNotFoundError("Не знайдено файл з ключами доступу до Google Таблиці!")

sheet = gc.open("ihor_huila").sheet1

# Токсичні та тупі перли Ігоря
igor_quotes = [
    "Я бельё-то принёс, но развешивать не умею... Короче, сделать ничего не могу, отстань.",
    "Зачем мне нормально учиться и работать в белую? Для этого же думать надо, напрягаться... Лучше пойду людей на бабки наёбывать.",
    "Я не хочу в этом разбираться. С этим не справится даже топовый кодер, не то что эта ваша бесплатная программка!",
    "Зачем мне думать? Лучше я заплачу 100 баксов кому-то, потому что для этого нужен специальный сервак, а у меня лапки.",
    " *Ме-е-е-е...* Эээ... Чего ты от меня хочешь? Я вообще ничего не понял, у меня мозг от пива ссохся."
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    random_quote = random.choice(igor_quotes)
    sheet.append_row([
        message.from_user.username or "Анонім",
        random_quote,
        "Запустил бота (но работать не хочет)"
    ])
    await message.answer(random_quote)

@dp.message()
async def handle_all_messages(message: types.Message):
    random_quote = random.choice(igor_quotes)
    sheet.append_row([
        message.from_user.username or "Анонім",
        message.text,
        random_quote
    ])
    await message.answer(f" *Ме-е-е-е...* {random_quote}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
