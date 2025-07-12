from aiogram import Router, F
from db_queries import get_categories,get_goods_by_catid,get_good_by_id
from keyboards import get_categories_kb,get_goods_kb
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery,InlineKeyboardButton
router = Router()
@router.callback_query(lambda c:c.data == "delete_message")
async def delete_message(callback:CallbackQuery):
    await callback.message.delete()
@router.callback_query(lambda c:c.data == "back_to_categories")
async def back_to_categories(callback:CallbackQuery):
    await callback.message.edit_text("Каталог:",reply_markup=get_categories_kb(await get_categories(router.pool),True))
    await callback.answer()
@router.callback_query(lambda c:c.data.startswith("category_"))
async def categories_handler(callback:CallbackQuery):
    cat_id=int(callback.data.split("_")[1])
    keyboard = get_goods_kb(await get_goods_by_catid(router.pool,cat_id),True)
    await callback.message.edit_text("Выберите товар:", reply_markup=keyboard)
    await callback.answer()
@router.callback_query(lambda c:c.data.startswith("good_"))
async def goods_handler(callback:CallbackQuery):
    id=int(callback.data.split("_")[1])
    good = await get_good_by_id(router.pool,id)
    text=(
    "━━━━━━━━━━━━━━━\n"
    "🛒 <b> Покупка </b>\n"
    "━━━━━━━━━━━━━━━\n\n"
    f"📦 <b>{good['name']}</b>\n"
    f"📝 Описание: {good['description']}\n"
    f"📦 Количество: {good['amount']} шт.\n"
    f"💰 Цена: {good['price']} руб.\n")
    await callback.message.edit_text(
        text,
        parse_mode="HTML"
    )
    await callback.answer()
    
@router.message(F.text.lower() == "товары")
@router.message(Command("goods"))
async def get_cat_list(message:Message):
    await message.answer("Каталог:",reply_markup=get_categories_kb(await get_categories(router.pool),True))
    
