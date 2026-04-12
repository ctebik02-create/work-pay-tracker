import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    button = InlineKeyboardButton(
        text = 'Open Work Tracker',
        web_app = WebAppInfo(url='https://work-pay-tracker.onrender.com')
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [[button]]
    )
    await message.answer(
        'Open your work tracker!',
        reply_markup = keyboard
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())