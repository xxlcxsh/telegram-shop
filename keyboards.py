from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
def get_categories_kb(categories: list[dict[str, str | int]], closebutton:bool) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text=f"{cat['emoji']} {cat['name']}",
            callback_data=f"category_{cat['id']}"
        )]
        for cat in categories
    ]
    if closebutton:
        buttons.append([InlineKeyboardButton(
            text="⬅️Назад",
            callback_data="delete_message"
        )])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_goods_kb(goods:list[dict[str, str | int]], backbutton: bool) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text=f"{good['name']}",
            callback_data=f"good_{good['id']}"
        )]
        for good in goods
    ]
    if backbutton:
        buttons.append([InlineKeyboardButton(
            text="⬅️Назад",
            callback_data="back_to_categories"
        )])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_y_or_n_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ]
    yn_keyboard=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    return yn_keyboard
def get_post_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Добавить товар")],
        [KeyboardButton(text="Добавить категорию")],
        [KeyboardButton(text="Пропустить")]
    ]
    p_keyboard=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    return p_keyboard
