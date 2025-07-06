from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from db_connect import get_pool
from db_queries import get_is_admin
from aiogram.fsm.context import FSMContext
from states.add_good_state import AddGood
router = Router()
@router.message(Command("admin_add_goods"))
async def add_good_start(message: Message, state: FSMContext):
    user=message.from_user
    pool = await get_pool()
    is_admin = await get_is_admin(pool,user.id)
    if is_admin:
        await message.answer("Доступ разрешен!\nВведите название товара.")
        await state.set_state(AddGood.waiting_for_name)
        
    else:
        await message.answer(
            "У вас нет прав доступа!"
        )
    await pool.close()
@router.message(AddGood.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddGood.waiting_for_desc)
@router.message(AddGood.waiting_for_desc)
async def get_desc(message:Message,state:FSMContext):
    await state.update_data(desc=message.text)
    await message.answer("Введите цену товара")
    await state.set_state(AddGood.waiting_for_price)
@router.message(AddGood.waiting_for_price)
async def get_price(message:Message,state:FSMContext):
    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Цена должна быть числом! Повторите ввод.")
        return None
    await state.update_data(price=price)
    await message.answer("Введите количество товара")
    await state.set_state(AddGood.waiting_for_amount)
@router.message(AddGood.waiting_for_amount)
async def get_amount(message:Message,state:FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Количество должно быть числом! Повторите ввод.")
        return None
    await state.update_data(amount=amount)
    await message.answer("Выберите категорию товара")
    await state.set_state(AddGood.waiting_for_category)
@router.message(AddGood.waiting_for_category)
async def get_category(message:Message,state:FSMContext):
    await state.update_data(category=message.text)
    data= await state.get_data()
    name=data["name"]
    desc=data["desc"]
    price=data["price"]
    amount=data["amount"]
    category=data["category"]
    kb = [
        [types.KeyboardButton(text="Да")],
        [types.KeyboardButton(text="Нет")]
    ]
    yn_keyboard=types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    await message.answer(f"Подтвердите добавление товара:\nНазвание: {name}\nОписание: {desc}\nЦена: {price} руб.\nКол-во: {amount}\nКатегория: {category}",reply_markup=yn_keyboard)
    await state.set_state(AddGood.waiting_for_confirm)
@router.message(AddGood.waiting_for_confirm)
async def get_confirm(message:Message,state:FSMContext):
    data = await state.get_data()
    name = data["name"]
    desc=data["desc"]
    price=data["price"]
    amount=data["amount"]
    category=data["category"]
    if message.text.lower() == "да":
        await message.answer(f"Товар {name} успешно добавлен ✅",reply_markup=types.ReplyKeyboardRemove())
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO goods (name,description,amount,price,category)
                VALUES ($1,$2,$3,$4,$5)
                """,
                name,desc,amount,price,category
            )
    elif message.text.lower() == "нет":
        await message.answer("добавление товара отменено ❌",reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")
        return None
    await state.clear()
    await pool.close()


    
        