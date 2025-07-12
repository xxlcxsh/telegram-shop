import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from db_queries import get_is_admin,get_all_users_id
from states.add_post_state import AddPost
from keyboards import get_post_kb,get_y_or_n_kb
router = Router()
def format_post(tittle, text):
    tittle = tittle.replace('-', '\\-').replace('.', '\\.').replace('!', '\\!')
    text = text.replace('-', '\\-').replace('.', '\\.').replace('!', '\\!')
    return f"*{tittle}*\n\n{text}"
@router.message(Command("admin.add_post"))
async def add_post_start(message:Message,state:FSMContext):
    user=message.from_user
    is_admin = await get_is_admin(router.pool,user.id)
    if is_admin:
        await message.answer("Введите название поста:")
        await state.set_state(AddPost.waiting_for_tittle)
    else:
        await message.answer("У вас неь прав доступа!")
@router.message(AddPost.waiting_for_tittle)
async def get_post_name(message:Message,state:FSMContext):
    await state.update_data(tittle=message.text)
    await message.answer("Введите текст поста:")
    await state.set_state(AddPost.waiting_for_text)
@router.message(AddPost.waiting_for_text)
async def get_post_text(message:Message,state:FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Дополнительно:",reply_markup=get_post_kb())
    await state.set_state(AddPost.waiting_for_add)
@router.message(AddPost.waiting_for_add)
async def get_post_add(message:Message,state:FSMContext):
    response=message.text.lower()
    data = await state.get_data()
    if response=="добавить товар":
        await message.answer(f"Вы собираетесь опубликовать пост:\n{format_post(data['tittle'],data['text'])}",reply_markup=get_y_or_n_kb())
        await state.set_state(AddPost.waiting_for_confirm)
    elif response=="добавить категорию":
        await message.answer(f"Вы собираетесь опубликовать пост:\n{format_post(data['tittle'],data['text'])}",reply_markup=get_y_or_n_kb())
        await state.set_state(AddPost.waiting_for_confirm)
    elif response=="пропустить":
        await message.answer(f"Вы собираетесь опубликовать пост:\n{format_post(data['tittle'],data['text'])}",reply_markup=get_y_or_n_kb())
        await state.set_state(AddPost.waiting_for_confirm)
    else:
        await message.answer("Пожалуйста, выберите один из вариантов")
@router.message(AddPost.waiting_for_confirm)
async def get_post_confirm(message:Message,state:FSMContext):
    if message.text.lower()=="да":
        was_sent=0
        data= await state.get_data()
        await message.answer(f"Пост опубликован ✅",reply_markup=ReplyKeyboardRemove())
        users = await get_all_users_id(router.pool)
        for user in users:
            try:
                await message.bot.send_message(user,format_post(data['tittle'],data['text']),parse_mode="MarkdownV2")
                was_sent+=1
                await asyncio.sleep(0.05)  # чтобы не получить flood limit
            except Exception as e:
                print(f"Ошибка отправки {user}: {e}")
        print(f"Сообщение отправлено {was_sent} пользователям")
    elif message.text.lower()=="нет":
        await message.answer("Публикация поста отменена ❌",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")
        return None
    await state.clear()