from aiogram.fsm.state import StatesGroup, State
class AddGood(StatesGroup):
    waiting_for_name = State()
    waiting_for_desc = State()
    waiting_for_price = State()
    waiting_for_amount = State()
    waiting_for_category = State()
    waiting_for_confirm = State()