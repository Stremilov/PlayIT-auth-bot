import asyncio
import logging
import os
from datetime import datetime

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
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


usernames = {1252614429: 'chml3', 5191163134: 'romashkaskrip', 821143465: 'nnnnastja', 809357333: 'vov_is',
             937774479: 'ilovepussycat', 1486670220: 'kkeysty', 930795438: 'kriingee', 943189828: 'MuWK4',
             504646530: 'malokohohoho', 915807931: 'abcdfpdf', 473166867: 'geoinkk', 1497908500: 'Enternal_Sun',
             1979271646: 'mapinlagor', 5273670174: 'b0brik666', 689929118: 'ivankrutoy45ru', 1612304869: 'rodiuynCK',
             5627142055: 'DungeonMaster300', 822262571: 'gerasandr', 649651569: 'luxage2',
             377428314: 'neveroyatneyshee',
             662985281: 'Diaonic7', 1328585666: 'sonkeiki', 5723224657: 'Akuzael', 1523135919: 'str_aa',
             1119645803: 'juxxccy',
             1031330795: 'solonchakovich', 621577849: 'suckfreaks', 862610257: 'my_name_is_freeman',
             1053669943: 'Bez_mozga8',
             1060346898: 'bll_nev_egor', 1442319699: 'VadimSyr1', 717870969: 'vel_toshik', 1052556039: 'vmataruev',
             1108697409: 'AquaRibka', 759372655: 'kymb6', 5183089093: 'altyn_aan', 762145175: 'aonens',
             1094272521: 'Aestesean',
             875605842: 'juliaviww9', 1045052354: 'hlebnoeizdelye', 1481198549: 'legiliem', 908492786: 'ziferus',
             948264674: 'lorenco09', 835614079: 'MaksimVee', 5472653434: 'design_slava', 1394695008: 'bmo_lorein',
             844979280: 'amsgcmh', 173728440: 'java_cg', 987969893: 'manyazur', 6435637532: 'jpeg667',
             1115514740: 'ddarriks',
             1537699104: 'StanislavLenskoy', 393900615: 'sever0277', 2130079840: 'blackpinkandegraund',
             950737324: 'minpolia',
             287356714: 'aleonenko', 464545175: 'peab0dy', 1085338647: 'Gorbachoo', 1403234441: 'Physc0',
             5673586582: 'IBabaKapal',
             1743566211: 'IIIyT_04ka', 5353133119: 'deV1cktor'}


@dp.message(Command("mailing"))
async def mailing_command(message: Message):
    whitelist = [294057781, 337683248, 659163860]
    tg_id = message.from_user.id
    text_to_mail = message.text[len('/mailing '):]
    if tg_id in whitelist:
        session = next(get_db_session())
        try:
            result = session.execute(text("SELECT telegram_id FROM users WHERE telegram_id IS NOT NULL"))
            telegram_ids = [row[0] for row in result.fetchall()]
            logging.info(f"Всего пользователей для рассылки: {len(telegram_ids)}")
            for tg_id in telegram_ids:
                try:
                    await bot.send_message(
                        chat_id=tg_id,
                        text=text_to_mail
                    )
                    await asyncio.sleep(0.05)
                except Exception as e:
                    logging.warning(f"Не удалось отправить сообщение {tg_id}: {e}")
        except Exception as e:
            logging.error(f"Ошибка при обращении к базе данных: {e}")
        finally:
            session.close()
    else:
        await message.answer('ты охуел?\n\nнет доступа!')


@dp.message(Command("mail_to_afk"))
async def cmd_register(message: Message):
    tg_id = message.from_user.id
    if tg_id == 294057781:
        await message.answer('начало рассылки людям')

        success_list, failed_list = [], []
        for user_id in usernames:
            try:
                await bot.send_message(chat_id=user_id, text='Здравствуй, странник!\n'
                                                             'Уже второй день мероприятия наступил, а тебя всё не видать 😪\n'
                                                             '\n'
                                                             'Отправь /start ещё раз и отправляйся в путь 🌳')
                success_list.append(usernames[user_id])
            except (TelegramForbiddenError, TelegramBadRequest):
                failed_list.append(usernames[user_id])
        await message.answer('разослано {} людям'.format(len(success_list)))
        await message.answer('не получилось разослать:\n'
                             '{}'.format(failed_list))

    else:
        await message.answer('ты охуел?\n\nнет доступа!')


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
        CronTrigger(hour=10, minute=0),
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
