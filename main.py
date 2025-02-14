import asyncio
import logging

from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "7609421759:AAFvZegHPaSRLNBLzwpsds5XZpuKVBUFfUI"
WEB_APP_URL = "https://it-otdel.space"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
    ],
        resize_keyboard=True
    )
    await message.answer(text="Привет! Нажми на кнопку, чтобы открыть приложение", reply_markup=keyboard,)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
