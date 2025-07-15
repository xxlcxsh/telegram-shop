from .add_category import router as cat_router
from .add_good import router as product_router
from .add_post import router as post_router
from .admin_manage import router as admin_router
from .add_data import router as data_router
from aiogram import Router
admin_routers = Router()
admin_routers.include_routers(cat_router,product_router,post_router,admin_router,data_router)

