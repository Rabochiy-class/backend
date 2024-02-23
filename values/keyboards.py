from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from values.strings import go_to_app, how_to_use, support
from config import WEBAPP_URL

web_app = WebAppInfo(url=WEBAPP_URL)

keyboard_builder = InlineKeyboardBuilder()
keyboard_builder.row(
    InlineKeyboardButton(
        text=go_to_app,
        web_app=web_app
    )
)
keyboard_builder.row(
    InlineKeyboardButton(
        text=how_to_use,
        callback_data='FAQ'
    )
)
keyboard_builder.row(
    InlineKeyboardButton(
        text=support,
        url='https://t.me/ShvetsovArtyom'
    )
)
