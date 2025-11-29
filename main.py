import os
import requests
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ✅ /start command
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    r = requests.get("https://api.quotable.io/random")
    quote = r.json()["content"]

    await message.answer(f"Я люблю Наргиз ❤️\n\nQuote:\n{quote}")

# ✅ Telegram Webhook Receiver
@app.post("/")
async def telegram_webhook(request: Request):
    update = types.Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}

# ✅ Auto-set Webhook on Deploy
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
