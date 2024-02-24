from aiogram.fsm.state import StatesGroup, State


class PhoneRequest(StatesGroup):
    waiting_for_phone = State()
