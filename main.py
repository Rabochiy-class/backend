import asyncio
import logging
import logging.config

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TOKEN, LOGGING_CONFIG, WEBAPP_URL

main_router = Router()
bot = Bot(token=TOKEN)
dp = Dispatcher()

logger = logging.getLogger(__name__)
web_app = WebAppInfo(url=WEBAPP_URL)


@main_router.message(Command("start"))
async def start_handler(message: Message):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text='Перейти к приложению',
            web_app=web_app
        )
    )

    await message.answer('<b>📍 Меню донора</b>\n\n'
                         'Чтобы открыть приложение, нажмите на кнопку ниже 🔽',
                         reply_markup=keyboard_builder.as_markup(),
                         parse_mode='html')


def setup_loggers():
    logging.config.dictConfig(LOGGING_CONFIG)


async def main():
    setup_loggers()

    logger.info('Starting with Telegram API key %s', TOKEN)

    dp.include_router(main_router)

    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(text='Открыть приложение', web_app=web_app))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
