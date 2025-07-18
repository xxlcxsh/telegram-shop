from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from services.db_queries import get_is_admin,insert_category
from aiogram.fsm.context import FSMContext
from states.add_category_state import AddCategory
from keyboards.reply import yn_kb
router = Router()
@router.message(Command("admin.add_category"))
async def add_category_start(message:Message,state:FSMContext,pool):
    user=message.from_user
    is_admin = await get_is_admin(pool,user.id)
    if is_admin:
        await message.answer("Введите название категории:")
        await state.set_state(AddCategory.waiting_for_name)
        
    else:
        await message.answer(
            "У вас нет прав доступа!"
        )
@router.message(AddCategory.waiting_for_name)
async def get_name(message:Message,state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отправьте emoji для категории:")
    await state.set_state(AddCategory.waiting_for_emoji)
@router.message(AddCategory.waiting_for_emoji)
async def get_emoji(message:Message,state:FSMContext):
    await state.update_data(emoji=message.text)
    data= await state.get_data()
    emoji = data["emoji"]
    name = data["name"]
    await message.answer(f"Подтвердите добавление категории:\nНазвание: {name}\nemoji: {emoji}",reply_markup=yn_kb())
    await state.set_state(AddCategory.waiting_for_confirm)
@router.message(AddCategory.waiting_for_confirm)
async def get_confirm(message:Message,state:FSMContext,pool):
    if message.text.lower()=="да":
        data= await state.get_data()
        await insert_category(pool,data["name"],data["emoji"])
        await message.answer(f"Категория {data['name']} успешно добавлена ✅",reply_markup=ReplyKeyboardRemove())
    elif message.text.lower()=="нет":
        await message.answer("Добавление категории отменено ❌",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")
        return None
    await state.clear()



    