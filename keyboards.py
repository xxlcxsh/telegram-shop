from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
def get_categories_kb(categories: list[dict[str, str | int]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text=f"{cat['emoji']} {cat['name']}",
            callback_data=f"category_{cat['id']}"
        )]
        for cat in categories
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_y_or_n_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ]
    yn_keyboard=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    return yn_keyboard