from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_BUTTONS_RU


def create_inline_kb(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_BUTTONS_RU[button] if button in LEXICON_BUTTONS_RU else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON_BUTTONS_RU[last_btn] if button in LEXICON_BUTTONS_RU else last_btn,
            callback_data=last_btn
        ))

    return kb_builder.as_markup()

def start_keyboard():
    return create_inline_kb(3, 'button_upload', 'button_avg_prices')
