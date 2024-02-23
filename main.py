import asyncio
import logging
import logging.config

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import TOKEN, LOGGING_CONFIG
from values.strings import menu, faq
from values.keyboards import keyboard_builder

main_router = Router()
bot = Bot(token=TOKEN)
dp = Dispatcher()

logger = logging.getLogger(__name__)


@main_router.callback_query()
async def main_callback_handler(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id,
                           text=faq,
                           parse_mode='html')
    await bot.send_message(chat_id=call.message.chat.id,
                           text=menu,
                           reply_markup=keyboard_builder.as_markup(),
                           parse_mode='html')


@main_router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(menu,
                         reply_markup=keyboard_builder.as_markup(),
                         parse_mode='html')


@main_router.message()
async def any_text(message: Message):
    await message.answer(menu,
                         reply_markup=keyboard_builder.as_markup(),
                         parse_mode='html')


def setup_loggers():
    logging.config.dictConfig(LOGGING_CONFIG)


async def main():
    setup_loggers()

    logger.info('Starting with Telegram API key %s', TOKEN)

    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
