from aiogram.filters.callback_data import CallbackData

class CategoryCallback(CallbackData, prefix="category"):
    category_id: int

class ProductCallback(CallbackData, prefix="product"):
    action: str
    product_id: int
class AddProduct(CallbackData,prefix="category_add"):
    category_id: int
class AddDataCategory(CallbackData,prefix="data_category"):
    action: str
    category_id: int
class AddDataProduct(CallbackData,prefix="data_product"):
    product_id: int
