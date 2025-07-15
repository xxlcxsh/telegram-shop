from aiogram.fsm.state import StatesGroup, State
class AddData(StatesGroup):
    waiting_for_data = State()
    waiting_for_good = State()
    waiting_for_confirm = State()