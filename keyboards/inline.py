from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_data.callbacks import ProductCallback,CategoryCallback,AddProduct
from services.db_queries import get_goods_by_catid,get_categories
def product_keyboard(product_id:int,category_id:int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="🛒 Купить",
                callback_data=ProductCallback(action="buy", product_id=product_id).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=CategoryCallback(category_id=category_id).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
async def category_keyboard(pool) -> InlineKeyboardMarkup:
    categories = await get_categories(pool)
    kb=[]
    for category in categories:
        kb.append([
            InlineKeyboardButton(
                text=category["emoji"]+" "+category["name"],
                callback_data=CategoryCallback(category_id=category["id"]).pack()
            )
        ])
    kb.append([
        InlineKeyboardButton(
            text="❌ Закрыть",
            callback_data="delete_message"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)
async def products_keyboard(pool,category_id) -> InlineKeyboardMarkup:
    products = await get_goods_by_catid(pool,category_id)
    kb=[]
    for product in products:
        kb.append([
            InlineKeyboardButton(
                text=product["name"],
                callback_data=ProductCallback(action="view", product_id=product["id"]).pack()
            )
        ])
    kb.append([
        InlineKeyboardButton(
            text="⬅️Назад",
            callback_data=CategoryCallback(category_id=0).pack()
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)
async def add_product_keyboard(pool):
    categories = await get_categories(pool)
    kb=[]
    for category in categories:
        kb.append([
            InlineKeyboardButton(
                text=category["emoji"]+" "+category["name"],
                callback_data=AddProduct(category_id=category["id"]).pack()
            )
        ])
    kb.append([
        InlineKeyboardButton(
            text="❌ Закрыть",
            callback_data="clear_state"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)