from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import asyncio, asyncpg
from config import TOKEN
from main_routers import add_good, profile, goods, add_funds, add_category, add_post
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)  
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(profile.router, goods.router,add_good.router, add_category.router,add_post.router)
async def on_startup(dispatcher: Dispatcher):
    pool = await asyncpg.create_pool(
        user='projuser',
        password='mypassword',
        database='ttest',
        host='localhost',
        port=5432
    )
    dispatcher.pool = pool
    profile.router.pool = pool
    goods.router.pool = pool
    add_funds.router.pool = pool
    add_good.router.pool = pool
    add_category.router.pool = pool
    add_post.router.pool = pool
    logging.info("Pool created")

async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.pool.close()
    logging.info("Pool closed")
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)
@dp.message(Command("start"))
async def start_handler(message: Message):
    kb=[    
        [types.KeyboardButton(text="Товары")],
        [types.KeyboardButton(text="Профиль")],
        [types.KeyboardButton(text="Пополнить баланс")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите действие:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())