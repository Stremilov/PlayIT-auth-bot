import asyncio
import logging
import os
from datetime import datetime
from sqlalchemy import text


import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from db import get_db_session

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


@dp.message(F.text == "moder_H2j8xO")
async def moder_button(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
    ],
        resize_keyboard=True
    )
    await message.answer(
        text="Привет! Нажми на кнопку, чтобы открыть приложение", reply_markup=keyboard
    )


# @dp.message(F.text == "rassilka_52")
# async def rassilka_from_db_sql(message: Message):
#     session = next(get_db_session())
#     try:
#         result = session.execute(text("SELECT telegram_id FROM users WHERE telegram_id IS NOT NULL"))
#         telegram_ids = [row[0] for row in result.fetchall()]
#
#         logging.info(f"Всего пользователей для рассылки: {len(telegram_ids)}")
#
#         keyboard = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
#         ],
#             resize_keyboard=True
#         )
#
#         for tg_id in telegram_ids:
#             try:
#                 await bot.send_message(
#                     chat_id=tg_id,
#                     text="Приветствую тебя, добрый молодец или девица красная! "
#                          "Дозволь уведомить о прибавлении новых заданий мудрёных.",
#                     reply_markup=keyboard
#                 )
#                 await asyncio.sleep(0.05)
#             except Exception as e:
#                 logging.warning(f"Не удалось отправить сообщение {tg_id}: {e}")
#     except Exception as e:
#         logging.error(f"Ошибка при обращении к базе данных: {e}")
#     finally:
#         session.close()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    # event_start_date = "11 апреля в 12:00"
    # event_start_datetime = datetime.strptime("2025-04-11", "%Y-%m-%d")
    #
    # current_datetime = datetime.now()
    #
    # if current_datetime < event_start_datetime:
    # await message.answer(
    #     "Здравствуй, странник!\n"
    #     "Это бот для участия в PlayIT 🧌\n"
    #     "После начала мероприятия именно здесь ты начнёшь своё сказочное путешествие!\n\n"
    #     f"Мероприятие начнётся {event_start_date}.\n\n"
    #     "Бот заработает в день начала мероприятия."
    # )
    # else:
    if check_user(message):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
        ],
            resize_keyboard=True
        )
        await message.answer(text="Привет! Нажми на кнопку, чтобы открыть приложение", reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению вы не зарегистрировались на это мероприятие.\n\nEсли вы заполняли форму, обратитесь в поддержку — @playit_2025")


async def send_daily_message():
    session = next(get_db_session())
    try:
        result = session.execute(text("SELECT telegram_id FROM users WHERE telegram_id IS NOT NULL"))
        telegram_ids = [row[0] for row in result.fetchall()]

        logging.info(f"Всего пользователей для рассылки: {len(telegram_ids)}")

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
        ],
            resize_keyboard=True
        )

        for tg_id in telegram_ids:
            try:
                await bot.send_message(
                    chat_id=tg_id,
                    text="Приветствую тебя, добрый молодец или девица красная! "
                         "Дозволь уведомить о прибавлении новых заданий мудрёных.",
                    reply_markup=keyboard
                )
                await asyncio.sleep(0.05)
            except Exception as e:
                logging.warning(f"Не удалось отправить сообщение {tg_id}: {e}")
    except Exception as e:
        logging.error(f"Ошибка при обращении к базе данных: {e}")
    finally:
        session.close()


async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_daily_message,
        CronTrigger(hour=12, minute=0),
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
