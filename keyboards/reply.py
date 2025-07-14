from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
def yn_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ]
    yn_keyboard=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    return yn_keyboard
def post_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Добавить товар")],
        [KeyboardButton(text="Добавить категорию")],
        [KeyboardButton(text="Пропустить")]
    ]
    p_keyboard=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    return p_keyboard
