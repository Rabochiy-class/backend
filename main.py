import asyncio
import logging
import logging.config

from aiogram import F
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, MenuButtonWebApp, WebAppInfo

from config import TOKEN, LOGGING_CONFIG, PAYMENT_TOKEN, WEBAPP_URL
from values.strings import menu, faq, donate_description, successful_payment_str
from values.keyboards import keyboard_builder

main_router = Router()
bot = Bot(token=TOKEN)
dp = Dispatcher()

web_app = WebAppInfo(url=WEBAPP_URL)

logger = logging.getLogger(__name__)


@main_router.callback_query(lambda callback_query: callback_query.data == 'support_bot')
async def order(call: CallbackQuery):
    """
    Sends invoice with payment settings.
    Here the user will pay, enter their card information, choose what sum to pay.
    :param call:
    :return:
    """
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title='❤️ Помочь проекту',
        description=donate_description,
        payload='Support DonorSearch',
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        prices=[
            LabeledPrice(
                label='100',
                amount=10000
            )
        ],
        max_tip_amount=90000,
        suggested_tip_amounts=[30000, 50000, 70000],
        start_parameter='donorSearch',
        provider_data=None,
        need_name=True,
        need_phone_number=True,
        need_email=True,

    )


@main_router.pre_checkout_query(lambda query: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    """
    A function that is necessary for the end of payment.
    :param pre_checkout_query:
    :return:
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@main_router.message(F.successful_payment)
async def successful_payment(call: CallbackQuery):
    """
    A function that is necessary for a successful payment.
    :return:
    """

    await call.answer(successful_payment_str, parse_mode='html')
    await call.answer(text=menu,
                      reply_markup=keyboard_builder.as_markup(),
                      parse_mode='html')


@main_router.callback_query(lambda callback_query: callback_query.data == 'faq')
async def faq_handler(call: CallbackQuery):
    """
    Handles "How to use bot" call.
    Shows =faq= message and main menu after it.
    :param call:
    :return:
    """
    await bot.send_message(chat_id=call.message.chat.id,
                           text=faq,
                           parse_mode='html')
    await bot.send_message(chat_id=call.message.chat.id,
                           text=menu,
                           reply_markup=keyboard_builder.as_markup(),
                           parse_mode='html')


@main_router.message(Command('start'))
async def start_handler(message: Message):
    """
    Handling '/start' command. Shows main menu with 3 buttons:
    - Go to web app
    - How to use bot
    - Support
    :param message:
    :return:
    """
    await message.answer(menu,
                         reply_markup=keyboard_builder.as_markup(),
                         parse_mode='html')


@main_router.message()
async def any_text(message: Message):
    """
    Handles any text that is not '/start', 'faq', 'support_bot'.
    Repeats main menu to user until they
    see the 'how to use' button and press it.
    :param message:
    :return:
    """
    await message.answer(menu,
                         reply_markup=keyboard_builder.as_markup(),
                         parse_mode='html')


def setup_loggers():
    logging.config.dictConfig(LOGGING_CONFIG)


async def main():
    """
    Sets up logging, starts dispatcher polling.
    :return:
    """
    setup_loggers()

    logger.info('Starting with Telegram API key %s', TOKEN)

    dp.include_router(main_router)

    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(text='Открыть приложение', web_app=web_app))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
