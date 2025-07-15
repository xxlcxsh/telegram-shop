from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import asyncio, asyncpg
from config import TOKEN
import logging
from handlers import routers
from middleware.db_middleware import DBMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)  

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
for router in routers:
    dp.include_router(router)

# Функция старта
async def on_startup(dispatcher: Dispatcher):
    pool = await asyncpg.create_pool(
        user='projuser',
        password='mypassword',
        database='ttest',
        host='localhost',
        port=5432
    )
    # Регистрируем middleware для всех роутеров и диспетчера
    dp.update.middleware(DBMiddleware(pool))
    logging.info("Pool created")

# Функция выключения
async def on_shutdown(dispatcher: Dispatcher):
    mw = next((m for m in dp.update.outer_middleware if isinstance(m, DBMiddleware)), None)
    if mw:
        await mw.pool.close()
    logging.info("Pool closed")
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)
@dp.message(Command("start"))
async def start_handler(message: Message):
    kb = [
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
