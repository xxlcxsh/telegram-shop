from aiogram.fsm.state import StatesGroup, State
class AddCategory(StatesGroup):
    waiting_for_name = State()
    waiting_for_emoji = State()
    waiting_for_confirm= State()