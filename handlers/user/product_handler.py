from aiogram import Router, F
from aiogram.types import Message,CallbackQuery
from callback_data.callbacks import ProductCallback
from keyboards.inline import product_keyboard
from services.db_queries import get_good_by_id
router=Router()
@router.callback_query(ProductCallback.filter())
async def products(callback:CallbackQuery,callback_data:ProductCallback,pool):
    if callback_data.action=="view":
        good = await get_good_by_id(pool,callback_data.product_id)
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
            parse_mode="HTML",
            reply_markup=product_keyboard(callback_data.product_id,good["category"])
        )
        await callback.answer()
    elif callback_data.action=="buy":
            await callback.message.answer("Спасибо за покупку")
            await callback.answer()
    else:
        await callback.answer("Неизвестное действие", show_alert=True)