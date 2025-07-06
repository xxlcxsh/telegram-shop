from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import asyncio
from token_telegram import TOKEN
from main_routers import profile,goods,add_funds,admin
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)  
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(profile.router, goods.router, add_funds.router,admin.router)

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