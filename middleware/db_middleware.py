from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class DBMiddleware(BaseMiddleware):
    def __init__(self, pool):
        self.pool = pool

    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["pool"] = self.pool
        return await handler(event, data)
