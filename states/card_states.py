from aiogram.fsm.state import State, StatesGroup

class CardStates(StatesGroup):
    waiting_for_card_data = State()
    waiting_for_additional_info = State()
