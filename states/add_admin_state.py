from aiogram.fsm.state import StatesGroup, State
class AddAdmin(StatesGroup):
    waiting_for_username = State()
    waiting_for_confirm= State()