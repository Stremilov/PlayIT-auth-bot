import asyncio
import logging
import os
from datetime import datetime

import pandas as pd
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEB_APP_URL = "https://it-otdel.space"

bot = Bot(token=TOKEN)
dp = Dispatcher()

CSV_FILE_PATH = "data.csv"


def check_user(message: Message):
    tg_username = message.from_user.username

    df = pd.read_csv(CSV_FILE_PATH)

    if tg_username in df['telegram_username'].values:
        return True

    return False


@dp.message(Command("start"))
async def start_cmd(message: Message):
    event_start_date = "11 апреля"
    event_start_datetime = datetime.strptime("2025-04-11", "%Y-%m-%d")

    current_datetime = datetime.now()

    if current_datetime < event_start_datetime:
        await message.answer(
            "Здравствуй, странник!\n"
            "Это бот для участия в PlayIT 🧌\n"
            "После начала мероприятия именно здесь ты начнёшь своё сказочное путешествие!\n\n"
            f"Мероприятие начнётся {event_start_date}.\n\n"
            "Бот заработает в день начала мероприятия."
        )
    else:
        if check_user(message):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
            ],
                resize_keyboard=True
            )
            await message.answer(text="Привет! Нажми на кнопку, чтобы открыть приложение", reply_markup=keyboard)
        else:
            await message.answer(text="К сожалению, вы не регистрировались на это мероприятие.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
