from .add_category import router as cat_router
from .add_good import router as product_router
from .add_post import router as post_router
from aiogram import Router
admin_router = Router()
admin_router.include_routers(cat_router,product_router,post_router)

