from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from values.strings import go_to_app, how_to_use, support, support_bot
from config import WEBAPP_URL

web_app = WebAppInfo(url=WEBAPP_URL)

"""
The main and only keyboard with 3 buttons:
- Go to web app (opens web app)
- How to use bot (shows message with instructions)
- Support (leads to one of the developers' telegram profile)
"""

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
        callback_data='faq'
    )
)
keyboard_builder.row(
    InlineKeyboardButton(
        text=support_bot,
        callback_data='support_bot'
    )
)
keyboard_builder.row(
    InlineKeyboardButton(
        text=support,
        url='https://t.me/ShvetsovArtyom'
    )
)
