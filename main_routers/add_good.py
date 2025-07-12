from aiogram import Router
from aiogram.filters import Command,StateFilter
from aiogram.types import Message,CallbackQuery, ReplyKeyboardRemove
from db_queries import get_is_admin,insert_good,get_categories
from keyboards import get_categories_kb,get_y_or_n_kb
from aiogram.fsm.context import FSMContext
from states.add_good_state import AddGood
router = Router()
@router.callback_query(lambda c:c.data.startswith("category_"),StateFilter(AddGood.waiting_for_category))
async def process_category_callback(callback:CallbackQuery,state:FSMContext):
    cat_id=int(callback.data.split("_")[1])
    await state.update_data(category_id=cat_id)
    data= await state.get_data()
    name=data["name"]
    desc=data["desc"]
    price=data["price"]
    amount=data["amount"]
    category_id=data["category_id"]
    await callback.message.answer(f"Подтвердите добавление товара:\nНазвание: {name}\nОписание: {desc}\nЦена: {price} руб.\nКол-во: {amount}\nID категории: {category_id}",reply_markup=get_y_or_n_kb())
    await callback.answer()
    await state.set_state(AddGood.waiting_for_confirm)
@router.message(Command("admin.add_goods"))
async def add_good_start(message: Message, state: FSMContext):
    user=message.from_user
    is_admin = await get_is_admin(router.pool,user.id)
    if is_admin:
        await message.answer("Введите название товара:")
        await state.set_state(AddGood.waiting_for_name)
        
    else:
        await message.answer(
            "У вас нет прав доступа!"
        )
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
    await message.answer("Выберите категорию товара",reply_markup=get_categories_kb(await get_categories(router.pool),False))
    await state.set_state(AddGood.waiting_for_category)
@router.message(AddGood.waiting_for_confirm)
async def get_confirm(message:Message,state:FSMContext):
    data = await state.get_data()
    name = data["name"]
    desc=data["desc"]
    price=data["price"]
    amount=data["amount"]
    cat_id=data["category_id"]
    if message.text.lower() == "да":
        await message.answer(f"Товар {name} успешно добавлен ✅",reply_markup=ReplyKeyboardRemove())
        await insert_good(router.pool,name,desc,amount,price,cat_id)
    elif message.text.lower() == "нет":
        await message.answer("Добавление товара отменено ❌",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")
        return None
    await state.clear()


    
        