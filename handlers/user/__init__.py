from .category_handler import router as cat_router
from .product_handler import router as product_router
from .user_profile import router as profile_router
from aiogram import Router
user_routers = Router()
user_routers.include_routers(cat_router,product_router,profile_router)