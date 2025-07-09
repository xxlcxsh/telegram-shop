from aiogram import Router, F
from db_connect import get_pool
from db_queries import get_categories
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
@router.message(lambda message: message.text and message.text.lower() == "товары")
@router.message(Command("goods"))
async def categories_list(message: Message):
    pool = await get_pool()
    categories = await get_categories(pool)
    keyboard = [
        
    ]