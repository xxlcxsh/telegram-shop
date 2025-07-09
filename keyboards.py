from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
def get_categories_kb(categories: list[dict[str, str | int]]) -> InlineKeyboardMarkup:
    keyboard=InlineKeyboardMarkup(row_width=2)
    buttons=[InlineKeyboardButton(
        text=cat['name'],
        callback_data=f"category_{cat['id']}"
        )
        for cat in categories
    ]
    keyboard.add(*buttons)
    return keyboard
def get_y_or_n_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ]
    yn_keyboard=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    return yn_keyboard