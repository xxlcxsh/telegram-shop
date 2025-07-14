from aiogram import Router
from services.db_queries import get_balance, get_spent, get_time_created, create_user
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
router = Router()
@router.message(lambda message: message.text and message.text.lower() == "профиль")
@router.message(Command("profile"))
async def profile_handler(message: Message,pool):
    user=message.from_user
    await create_user(pool,user.id)
    balance = await get_balance(pool,user.id)
    spent = await get_spent(pool,user.id)
    time_created = await get_time_created(pool,user.id)
    await message.answer(
        f"Баланс: {balance} руб.\nВсего потрачено: {spent} руб.\nДата регистрации: {time_created.strftime('%d-%m-%Y')}",
        reply_markup=ReplyKeyboardRemove()
    )