from aiogram import Router, F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from callback_data.callbacks import CategoryCallback
from keyboards.inline import category_keyboard,products_keyboard
router=Router()
@router.message(F.text.lower() == "товары")
@router.message(Command("goods"))
async def products(message:Message,pool):
    await message.answer("📦 Каталог:",reply_markup=await category_keyboard(pool))
@router.callback_query(lambda c:c.data == "delete_message")
async def delete_message(callback:CallbackQuery):
    await callback.message.delete()
@router.callback_query(CategoryCallback.filter())
async def category_handler(callback:CallbackQuery,callback_data:CategoryCallback,pool):
    if callback_data.category_id == 0:
        await callback.message.edit_text("📦 Каталог:",reply_markup=await category_keyboard(pool))
    else:
        await callback.message.edit_text(
            "Товары",
            reply_markup=await products_keyboard(pool,callback_data.category_id)
        )
    await callback.answer()