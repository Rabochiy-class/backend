from config import bot
from config import dp

from asyncio import run

from aiogram import *
from aiogram.filters import Command

main_router = Router()


@main_router.message(Command("start"))
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="hello")


async def main():
    await dp.start_polling(bot)


dp.include_router(main_router)

if __name__ == "__main__":
    run(main())
