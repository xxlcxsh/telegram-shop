from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from services.db_queries import get_is_admin,add_admin
from states.add_admin_state import AddAdmin
from keyboards.reply import yn_kb
from aiogram.exceptions import TelegramBadRequest
router=Router()
@router.message(Command("admin.add_admin"))
async def add_admin(message:Message,state:FSMContext,pool):
    is_admin = await get_is_admin(pool,message.from_user.id)
    if is_admin:
        await message.answer("Введите Telegram ID (не @username)")
        await state.set_state(AddAdmin.waiting_for_username)
    else:
        await message.answer(
            "У вас нет прав доступа!"
        )
@router.message(AddAdmin.waiting_for_username)
async def get_username(message:Message,state:FSMContext):
    await state.update_data(username=int(message.text))
    await message.answer("Подтвердите добавление:",reply_markup=yn_kb())
    await state.set_state(AddAdmin.waiting_for_confirm)
@router.message(AddAdmin.waiting_for_confirm)
async def get_confirm(message:Message,state:FSMContext,pool):
    if message.text.lower() == "да":
        try:
            data= await state.get_data()
            new_admin_id = data["username"]

            if await get_is_admin(pool,new_admin_id):
                await message.answer("✅ Этот пользователь уже админ.",reply_markup=ReplyKeyboardRemove())
            else:
                await add_admin(new_admin_id,pool)
                await message.answer(f"✅ Пользователь @{data["username"]} добавлен в админы.",reply_markup=ReplyKeyboardRemove())

        except TelegramBadRequest:
            await message.answer(f"⚠️ Не удалось найти @{data["username"]}. Он должен написать боту или быть в чате.",reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            await message.answer(f"⚠️ Произошла ошибка: {e}",reply_markup=ReplyKeyboardRemove())
    elif message.text.lower() == "нет":
        await message.answer("Добавление отменено ❌",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")
        return None
    await state.clear()
