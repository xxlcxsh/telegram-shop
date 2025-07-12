from aiogram.fsm.state import StatesGroup, State
class AddPost(StatesGroup):
    waiting_for_tittle = State()
    waiting_for_text = State()
    waiting_for_add= State()
    waiting_for_confirm = State()