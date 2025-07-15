import os
from aiogram import Router
import aiofiles
from aiogram.filters import Command,StateFilter
from aiogram.types import Message,CallbackQuery, ReplyKeyboardRemove
from services.db_queries import get_is_admin,process_file
from callback_data.callbacks import AddDataCategory,AddDataProduct
from keyboards.inline import data_category_keyboard,data_product_keyboard
from keyboards.reply import yn_kb
from aiogram.fsm.context import FSMContext
from states.add_data_state import AddData
router=Router()
@router.callback_query(AddDataCategory.filter(), StateFilter(AddData.waiting_for_good))
async def get_category(callback: CallbackQuery, state: FSMContext, callback_data: AddDataCategory, pool):
    if callback_data.action == "delete":
        await callback.message.delete()
        await state.clear()
    else:
        await callback.message.answer(
            "Выберите товар:",
            reply_markup=await data_product_keyboard(pool, callback_data.category_id)
        )
    await callback.answer()
@router.callback_query(AddDataProduct.filter())
async def get_product(callback: CallbackQuery, state: FSMContext, callback_data: AddDataCategory,):
    await state.update_data(product_id=callback_data.product_id)
    await callback.message.answer("Подтвердите добавление данных",reply_markup=yn_kb())
    await callback.answer()
    await state.set_state(AddData.waiting_for_confirm)
@router.message(Command("admin.add_data"))
async def add_data_start(message:Message,state:FSMContext,pool):
    is_admin = await get_is_admin(pool,message.from_user.id)
    if is_admin:
        await message.answer("Отправьте txt файл, где в каждой строке указаны данные одной единицы товара")
        await state.set_state(AddData.waiting_for_data)
        
    else:
        await message.answer(
            "У вас нет прав доступа!"
        )
@router.message(AddData.waiting_for_data)
async def get_data(message:Message,state:FSMContext,pool):
    if not message.document:
        await message.answer("Пожалуйста, пришлите .txt файл.")
        return
    if not message.document.file_name.endswith('.txt'):
        await message.answer("Принимаются только .txt файлы.")
        return
    file = await message.bot.get_file(message.document.file_id)
    file_path = f"temp/{message.document.file_name}"
    os.makedirs("temp", exist_ok=True)
    await message.bot.download_file(file.file_path, file_path)
    await state.update_data(file_path=file_path)
    await message.answer("Выберите категорию:",reply_markup=await data_category_keyboard(pool))
    await state.set_state(AddData.waiting_for_good)
@router.message(AddData.waiting_for_confirm)
async def get_confirm(message:Message,state:FSMContext,pool):
    data = await state.get_data()
    if message.text.lower() == "да":
        file_path = data.get("file_path")
        product_id=data["product_id"]
        if not file_path:
            await message.answer("Нет загруженного файла.")
            return
        count = await process_file(file_path,product_id,pool)
        await message.answer(f"Файл обработан, строк загружено: {count}")
        os.remove(file_path)
    elif message.text.lower() == "нет":
        await message.answer("Добавление данных отменено ❌",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")
        return None
    await state.clear()


