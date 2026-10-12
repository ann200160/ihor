import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Твій токен від BotFather
TOKEN = "8961643403:AAEjGi3G482HtvxR1CFyF-YMErsoVlJo3DI"

# Налаштування Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Дані сервісного акаунта
credentials_dict = {
    "type": "service_account",
    "project_id": "ihorhuila",
    "private_key_id": "4ac2f59609401da04f71a5d2a7326f9a60f1f5d8",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQDrNqJP10sv6Lab\n/Va7mfjlE8KzUxaU0rwCFiZzn6HQdnKsn+t6l09ILpyzn6Thx3uj9PamPns1dkji\nDdw3TJ5GeME7oF+4pgck7HbYxpd0ZjN8A6GhwmnH70ND9aPkeum6lDyWNJWBxdyb\n4iL6uxDpdyJECQ67Rpcb4AcNkT9gAeCIhLb84ygw2Pkwn03m61tmFTyJdBgyjUAa\nUG3StcKe3+Ba97WE8WzGlPIi3MfwdeyoKsggKiFcgRM8FVfnsRK6vkH43qayf5FK\nXj5WFM4KyRTJ9ra+FOjafX/Z9c0LOqyJbsTamiuZFVNjoCKzeErBmYvffOXqwado\nDP0scOEBAgMBAAECgf8Iun5LeDHSFVCxeTU+wPf7iEAxZ2PvIeLYMPo8UDAxDDQ1\nM7oJUpQemZw3DjWQK1brPqvof2kTEtChkuIZKz60XsbM76ads4uQUzYV1UjJiQFg\nGMJmvlAumzJj0znBwM3rnpSg/lKN/kmxfzLNGyQFheY/oBZr3LK+1hFs73bqmRUC\nuGna2XJJaMa0Tb6IalMZTgevAeaA7Qtt1wiB3umdIq9SRkpY8Z7gNmbSp5O6Q9qp\nkvyO+20D+gXysgnTZMd7h++W676w/KvgEQ1jNLZEB05dE9Z06Ibt2In6QBTQtc4x\ntx0CqNkkgn9e7HeKVdE0evXDS9mhBpx7naMkad8CgYEA/jiE8fyyuh3CUUJJXOe7\njlcCO814hjfxVwd2XAn7Ojq5gkTWALEuP3W9VtX8SekdK3+TVfN0MT7abq+53JPJ\nSb5PBO7/atJSQv34j85D8GumZqdJu/+vr/gRt2jGNL9RaH8HhrmlvgyY3roOef8f\n4DnNP7YYpvGgQl/1kZhDCPMCgYEA7NwPSbW8hVpYVAchbqoLOHdgX1yodrvrc7el\nMNjKKn3NejIsKs1zMizrE5w0B/CnZMw1HcHD1Ts5zv+6KenybgGMYjYnEG4jh+er\nAJvOLzpWo5GaFMU9PUQpRnbdKr1RzVqvzEIFtj94rcajgUBpuknizFhhM4M13g9y\nf5LPKzsCgYBLEjOoJgA9V7ZfOpzhc4j+QpFlSYrSz8hT898u1L+8dUT8xAkSEUBf\n+wvbjbs/tDgp9TV0Bz2DoVTtpLTU/0tMnIdHJLCGQe+K2ubAyJ9latSrsbDjdGDU\nLQRGTglh4DFRE1oMndvk4GFwPC80NXObSlZi/woOmoHBuAaTZQw+owKBgBroQOBZ\nwenQQpqBGN4ueQnYHd2XdBfQ70V9BkoPRqAfHHmWO4g9QKnhim723r5MK2f6/sm7\nmlid2spWKLrcNcsjZ+Q8TKHEMUseGUH/cSPSV8dLIhrb8UIFfT7g/+z8Bs/yTmhA\n089JVJdBKo/jVl9wR1B5dclZTYRFcvdlIR3DAoGAJww/RbyK+wa83SGwzJeBE/Fj\nOOfuN1WCmmYRyCHth0WfD4dOk9guHMUFlqrtpNcFFoKg7qSgfVqzpFQxp27UTLTd\nwutmyQRgXKCSCDUf1C1dC1+b3JqMTLDAI9Siv4NFhSnbjsZuObOmy9JT4dYbrMuz\nc15uHpAIuS3+KBUN7Bg=\n-----END PRIVATE KEY-----\n",
    "client_email": "ihor-huila-bot@ihorhuila.iam.gserviceaccount.com",
    "client_id": "110889341775890350063",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ihor-huila-bot%40ihorhuila.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Підключення до твоєї Google Таблиці ihor_huila
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("ihor_huila").sheet1

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
