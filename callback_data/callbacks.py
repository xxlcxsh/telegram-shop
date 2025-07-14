from aiogram.filters.callback_data import CallbackData

class CategoryCallback(CallbackData, prefix="category"):
    category_id: int

class ProductCallback(CallbackData, prefix="product"):
    action: str
    product_id: int
class AddProduct(CallbackData,prefix="category_add"):
    category_id: int
