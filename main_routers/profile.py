from aiogram import Router
from db_connect import get_pool
from db_queries import get_balance, get_spent, get_time_created, create_user
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
router = Router()
@router.message(lambda message: message.text and message.text.lower() == "профиль")
@router.message(Command("profile"))
async def profile_handler(message: Message):
    user=message.from_user
    pool = await get_pool()
    await create_user(pool,user.id)
    balance = await get_balance(pool,user.id)
    spent = await get_spent(pool,user.id)
    time_created = await get_time_created(pool,user.id)
    await message.answer(
        f"Баланс: {balance} руб.\nВсего потрачено: {spent} руб.\nДата регистрации: {time_created}",
        reply_markup=ReplyKeyboardRemove()
    )